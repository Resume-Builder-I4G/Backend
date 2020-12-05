# # '''Module that handles view of everything that has to do with mailing'''
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.image import MIMEImage
# from email import encoders
# import smtplib, ssl
# from socket import gaierror
# from app import app

# def send_mail(subject, recipient, text, html, pdf_attachment=None, pdf_name=None, image_attachment=None):
#     context = ssl.create_default_context()
#     message = MIMEMultipart("alternative")
#     message["Subject"] = subject
#     message['from'] = app.config['MAIL_USERNAME']
#     message['to'] = recipient
#     part1 = MIMEText(text, "plain")
#     part2 = MIMEText(html, "html")
#     message.attach(part1)
#     message.attach(part2)
#     if pdf_attachment:
#         part = MIMEBase("application", "octet-stream")
#         part.set_payload(attachment.read())
#         encoders.encode_base64(part)
#         part.add_header(
#                 "Content-Disposition",
#                 f"attachment; filename= {filename}",
#         )
#         message.attach(part)
#     if image_attachment:
#         image = MIMEImage(fp.read())
#         image.add_header('Content-ID', '<AiderLogo>')
#         message.attacg(image)
#     try:
#         with smtplib.SMTP_SSL(app.config['MAIL_SERVER'], app.config['MAIL_PORT'], context=context) as server:
#             server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
#             server.sendmail(app.config['MAIL_USERNAME'], 
#                             recipient, message.as_string())

#         print('Email sent!')

#     except (gaierror, ConnectionRefusedError):
#         return('Failed to connect to the server. Bad connection settings?')
        
#     except smtplib.SMTPServerDisconnected:
#         return('Failed to connect to the server. Wrong user/password?')

#     except smtplib.SMTPException as e:
#         return('SMTP error occurred: ' + str(e))

#     except Exception as e:
#         return('Something went wrong...'+str(e))


# '''Module that handles view of everything that has to do with mailing'''
import smtplib
from socket import gaierror
# from flask import current_app as app
from app import app, mail
from flask_mail import Message

def send_mail(subject, recipient, text, html, pdf_attachment=None, pdf_name=None, image_attachment=None):
    try:
        msg = Message(
            subject=subject, 
            sender='koikibabatunde14@gmail.com',  
            recipients=[recipient]
        )
        msg.body=text
        msg.html=html
        mail.send(msg)

    except (gaierror, ConnectionRefusedError):
        return('Failed to connect to the server. Bad connection settings?')
        
    except smtplib.SMTPServerDisconnected:
        return('Failed to connect to the server. Wrong user/password?')

    except smtplib.SMTPException as e:
        return('SMTP error occurred: ' + str(e))

    except Exception as e:
        return('Something went wrong...'+str(e))