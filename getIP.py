from os import path
from os import system
import sys
import urllib
import re
import smtplib as smtp
from email.mime.text import MIMEText

script_dir = path.dirname(__file__) # Directory of the script
userFname = "id" # Name of the file where user credentials are stored
ipFname = "ipaddr"
try:
    userFile = open(path.join(script_dir, userFname), 'r')
    ipFile = open(path.join(script_dir, ipFname), 'r+')
except:
    print("Can't open file, exit\n")
    sys.exit(-1)

username = userFile.readline().rstrip('\n')
password = userFile.readline().rstrip('\n')
netid = userFile.readline().rstrip('\n')

lastIP = ipFile.readline().rstrip('\n')

#Regular expression for matching *.*.*.*
ip_re = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}") 
try:
    #Search duckduckgo.com for ip and fetch the instant answer
    sock = urllib.urlopen("https://duckduckgo.com/?q=my+ip&ia=answer")

    htmldata = sock.read()
    ip = ip_re.search(htmldata)

    if ip:
        if lastIP == ip.group(0):
            sys.exit(0)
        else:
            print(ip.group(0))

            msg = MIMEText(str(ip.group(0)))
            msg['Subject'] = "IP"
            msg['From'] = username
            msg['To'] = msg['From']

            server = smtp.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(username, password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()

            ipFile.seek(0)
            ipFile.write(str(ip.group(0)))
            ipFile.truncate()
            ipFile.close()
            userFile.close()

except Exception, e:
    system("nmcli dev disconnect iface wlan0")
    system("nmcli con up id " + str(netid)) 
    userFile.close()
    ipFile.close()
    print e
