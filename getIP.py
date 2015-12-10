import urllib
import re
import smtplib as smtp
from email.mime.text import MIMEText

try:
    userFile = open('id', 'r')
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
        print ip.group(0)
        msg = MIMEText(ip.group(0))
        msg['Subject'] = "IP"
        #change this to read from file
        msg['From'] = "adwait.d10@gmail.com"
        msg['To'] = msg['From']

        server = smtp.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(msg['From'], msg['To'],str(ip.group(0)))
        server.quit()

except Exception, e:
    print e
    print("Can't connect to internet")
