# BootEmailer.py
#   Version: V1.1 - 2019-05-19
#   Author: Gary Davis (gary@webguild.com)

# Python3 script to send email when Pi boots with Pi's IP Address
# and the SSID of the connected WiFi.
#
# Add this to end of root's crontab to run this at boot time:
#   > sudo crontab -e
#   @reboot sudo /usr/bin/python3 ~pi/bin/BootEmailer.py > ~pi/logs/BootEmailer.log 2>&1

import smtplib
import subprocess
from email.mime.text import MIMEText
from time import sleep

# Set the your parameters such as email addresses, smtp server and credentials, etc.
mailServer = "smtp.gmail.com"
mailPort = 587
mailLogin = "youremail@gmail.com"
mailPassword = "abcdefsdxjkzrxyz" # If you use 2FA, this should be your App Password
mailFrom = "youremail@somewhere.com"
mailTo = "youremail@gmail.com, youremail@somewhere.com" # May have multiple delimited with commas

for i in range(30): # Keep trying till it works (up to 1 min)
	response = subprocess.run("hostname -I", stdout=subprocess.PIPE,
		shell=True, universal_newlines=True)
	ipAddr = response.stdout.strip()
	if (not (ipAddr == "" or ipAddr.startswith("169.256."))): # Break when legit DHCP-assigned IP addr
		break;
	print("Wait 2 seconds..." + ipAddr)
	sleep(2) # Wait for hostname and DNS for SMTP call

response = subprocess.run("hostname", stdout=subprocess.PIPE,
	shell=True, universal_newlines=True)
hostName = response.stdout.strip()

response = subprocess.run("iwgetid -r", stdout=subprocess.PIPE,
	shell=True, universal_newlines=True)
ssid = response.stdout.strip()

my_ip = hostName + ' IP is ' +  ipAddr + ' and connected to SSID "' + ssid + '"'
#my_ip = f'{hostName} IP is {ipAddr} and connected to WiFi SSID "{ssid}"' # Python 3.6+
msg = MIMEText(my_ip)
msg['From'] = mailFrom
msg['To'] = mailTo
msg['Subject'] = my_ip

s = smtplib.SMTP(mailServer, mailPort)
#s.set_debuglevel(1)
s.ehlo()
s.starttls()
s.login(mailLogin, mailPassword)
s.sendmail(mailFrom, [mailTo], msg.as_string())
s.quit

print (msg.as_string())
