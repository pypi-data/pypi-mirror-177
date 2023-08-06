# WillSpeak - Work in Progress
Python Text to Speach using Microsoft Sapi5 with a server/client model.

# Progress update
The core functionality is now working, and is ready for testing.
Some cleanup is still required, but it works.
Only supports SAPI5 for now. More to come in the future.

# Info
I created this project as a way to have good TTS on linux, because TTS on linux at the moment is dreadful.
For a long time I wanted to switch to linux, but I needed a good linux TTS software but could not find one.
So I decided to create this project to interface with the windows SAPI5 TTS engine.

How it works is by running this software in server mode on a Windows machine. 
Then configure the linux client to communicate with that Windows TTS server.
The client will monitor for text that was copied to the clipboard and converts the text into speech.

# Usage
This software has 2 different operational modes, "Local" & "Server/Client". If the TTS engine that you have selected 
works natively on your operating system, Then you can use Local mode. e.g. SAPI5 is native to windows, so you can use
Local mode on Windows when using SAPI5. You should use Server/Client if you want to use SAPI5 on linux.

Run locally on Windows
```shell
willspeak local
```

To run in server mode do.
```shell
willspeak server
```

And on the client machine run. "--addr" is the address of the server running the server component.
```shell
# 192.168.1.60 is just an example
willspeak client --addr=192.168.1.60
```

There is one last command that is used to stop any current speech.
```shell
willspeak stop
```

# TODO
* Use a string library to analyze and filter the text before converting.
* Setup prometheus metrics to track usage. This is useful if you wish to use a paid for TTS Service.
* Add support for other text to speech engines like eSpeak.
* Add support for running the server component as a Windows service.

# Links
https://winaero.com/unlock-extra-voices-windows-10/

## Version
0.3.0
