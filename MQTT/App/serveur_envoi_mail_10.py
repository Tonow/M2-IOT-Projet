# Import smtplib for the actual sending function
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import time

import setting

def envoi_mail(message = "corps du message"):
    time.sleep( 2 )
    msg = MIMEMultipart()
    msg['To'] = setting.client
    msg['Subject'] = "Rapport " + setting.nom_entreprise + ": " + str(datetime.now().date())
    msg.preamble  = 'Message de ' + setting.nom_entreprise
    msg.attach(MIMEText(message))

    for file in os.listdir('.'):
        if file.endswith(".png") and file.startswith("v"):
            if setting.debug:
                print(file)
            with open(file, 'rb') as fp:
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

    try:
        server.send_message(msg)
        print ('email sent')
    except:
        print ('error sending mail')

    server.quit()
