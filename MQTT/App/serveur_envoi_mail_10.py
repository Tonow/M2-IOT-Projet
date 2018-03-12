# Import smtplib for the actual sending function
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import setting


msg = MIMEMultipart()
# TO = input('Adresse client : ')
msg['To'] = "thomas.nowicki@hotmail.fr"
msg['Subject'] = 'TEST MAIL Python'
msg.preamble  = 'Message de python.'
msg.attach(MIMEText("corps du message"))

with open("Volume_Company_home_SDB..png", 'rb') as fp:
    img = MIMEImage(fp.read())
msg.attach(img)

# Gmail Sign In
gmail_sender = "master2.isc.usmb@gmail.com"
msg['From'] = gmail_sender
gmail_passwd = input('Mot de passe : ')

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(gmail_sender, gmail_passwd)

# BODY = '\r\n'.join(['To: %s' % TO,
#                     'From: %s' % gmail_sender,
#                     'Subject: %s' % SUBJECT,
#                     '', TEXT])

try:
    # server.sendmail(gmail_sender, [TO], BODY)
    server.send_message(msg)
    print ('email sent')
except:
    print ('error sending mail')

server.quit()
