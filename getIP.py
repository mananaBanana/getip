from os import path
import sys
import urllib
import re
import smtplib as smtp
from email.mime.text import MIMEText

script_dir = path.dirname(__file__) # Directory of the script
userFile_name = "id" # Name of the file where user credentials are stored
try:
    userFile = open(path.join(script_dir, userFile_name), 'r')
except:
    print("Can't open file, exit\n")
    sys.exit(-1)

username = userFile.readline().rstrip('\n')
password = userFile.readline().rstrip('\n')

#Regular expression for matching *.*.*.*
ip_re = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}") 
try:

    #Search duckduckgo.com for ip and fetch the instant answer
    sock = urllib.urlopen("https://duckduckgo.com/?q=my+ip&ia=answer")

    htmldata = sock.read()
    ip = ip_re.search(htmldata)

    if ip:
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

except Exception, e:
    print e
