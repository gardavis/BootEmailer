# BootEmailer

This is a python3 script to put on your Raspberry Pi so when it boots up, the script will run and send an email to you with its IP address and the SSID of the connected WiFi.

This is useful when you are at meetup/hackathon events where you may not know the connection information for your VNC Viewer when running your Raspberry headless.

The root crontab is set up to start the script on a boot. The script will keep trying to obtain the IP address until successful. This could take about 10 seconds (Raspberry Pi Zero, for example).

First, copy the BootEmailer.py script to your home/bin folder (or whereever you want). Create a home/logs folder to hold a log file created by the script for
debugging.

Next, edit the script to specify your parameters near the top of the file. You will specify the following. This example uses gmail to do the email sending:

* mailServer = "smtp.gmail.com"
* mailPort = 587
* mailLogin = "youremail@gmail.com"
* mailPassword = "abcdefsdxjkzrxyz"
* mailFrom = "youremail@somewhere.com"
* mailTo = "youremail@gmail.com, youremail@somewhere.com"

The mailLogin and mailPassword are your credentials to the smtp server (gmail in this case). If you use 2FA (2-factor authentication) for Google, this would be your App Password, otherwise it would be your regular password.

You may specify multiple email recipients delimited by commas if desired.

Run the script to try it out (assuming logged in as user pi):

	python3 ~pi/bin/BootEmailer.py
	
Verify there are no errors and that you receive the emails.

Finally, once you have verified the script with your parameters is working, you
have to add an entry to root's crontab to get the script to run when the Pi boots up.

Start up the crontab editor for root:

	sudo crontab -e

Add this line to the end of the crontab file

	@reboot sudo /usr/bin/python3 ~pi/bin/BootEmailer.py > ~pi/logs/BootEmailer.log 2>&1

That assumes the script is in user pi's bin folder. Adjust the command as needed.
