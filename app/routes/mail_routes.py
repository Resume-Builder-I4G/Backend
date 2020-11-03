'''Module that handles view of everything that has to do with mailing'''

import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app import app
# set up the SMTP server

from email.message import EmailMessage

def send_mail(user, body, subject):
        
    msg = EmailMessage()
    msg.set_content(msg)
    msg["Subject"] = subject
    msg["From"] = app.config['MAIL_USERNAME']
    msg["To"] = user
    context=ssl.create_default_context()

    with smtplib.SMTP(app.config['MAIL_SERVER'], port=app.config['MAIL_PORT']) as smtp:
        smtp.starttls(context=context)
        smtp.login(msg["From"], app.config['MAIL_PASSWORD'])
        smtp.send_message(msg)