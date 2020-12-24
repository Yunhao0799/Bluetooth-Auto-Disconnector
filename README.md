# Bluetooth Auto Disconnector

MacOS only

Simple command line script that automatically disconnect a bluetooth device or a bunch of them.

The reason after this project is after buying my Sony WH-1000XM3 I was constantly
forgetting to turn it off, causing battery drain.
This script adds the MAC-Address of the bluetooth device, after X minutes
without audio playing, it will disconnect the bluetooth device. In my case,
the headphones when detects it was disconnected for 5 minutes, it automatically
powers off.

## Installation

Requieres [BluetoothConnector](https://github.com/lapfelix/BluetoothConnector), I'm not the owner of it, 
to work.

After that, run the Python script:  
```python3 main.py```

Giving execution permission may be requiered to run the previous command, using the following commands:  
```chmod +x main.py```  
```chmod +x check_audio_playing.sh```  

Enjoy! :)
