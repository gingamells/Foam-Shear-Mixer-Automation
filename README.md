# Foam-Shear-Mixer-Automation

**Title:** 
Foam Shear Mixer Automation

**Introduction:** 
Microcontroller code via CircuitPython to automate the foam shear mixer

**How to install:** 
Plug in microcontroller (Metro M4 Express) via microUSB cable. If the microcontroller is named "METROM4BOOT" in the file explorer, then download [CircuitPython](https://circuitpython.org/board/metro_m4_express/), and drag the file onto the microcontroller name. The microcontroller should then become renamed as "CIRCUITPY". Download and drag the script onto the microcontroller, ensuring it is named "code.py". Overwrite the file on the microcontroller if neccessary.

**How to use:** 
TBD

**Technologies used:** 
TBD

**Features:** 
1- Autostart
	The AutoFOAM program runs on boot.
	To stop this feature temporarily, execute: "sudo systemctl stop autoFOAM"
	To disable this feature on next boot, type in the terminal: "sudo systemctl disable AutoFOAM.service".
	To check on the status & errors of the autostart service type in "sudo systemctl status AutoFOAM.service". Press Ctrl-C to exit status.
	To modify the autostart feature (i.e. execute a different python script, modify restart ability or frequency, change monitor), execute the following "sudo nano /etc/systemd/system/AutoFOAM.service" then reboot by executing "sudo reboot"
	Currently the Autostart is set to execute the program living in /home/pi/AF/GUI.py
	
