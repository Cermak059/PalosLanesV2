import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

def SendEmail(to, subject, body):
    username = "donotreply@paloslanes.net"
    password = "$D0!otBowl!2020"
    server = "smtp.paloslanes.net"
    port = 587

    msg = MIMEMultipart()
    msg['From'] = "donotreply@paloslanes.net"
    msg['To'] = to
    msg['Subject'] = subject

    html  = body
    msg.attach(MIMEText(html, 'html'))

    try:
        server = smtplib.SMTP_SSL(server, port)
        server.login(username, password)
        server.sendmail(username, to, msg.as_string())
    except Exception as e:
        return e
    finally:
        server.quit()


#if __name__== "__main__":
    #SendEmail("Wicket8688@gmail.com", "verify email", "verify")
    
