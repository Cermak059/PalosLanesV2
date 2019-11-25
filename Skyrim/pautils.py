import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

def SendEmail(to, subject, body):
    username = "Cermak059"
    password = "Pieman1993!"
    server = "smtp.comcast.net"
    port = 587

    msg = MIMEMultipart()
    msg['From'] = "Cermak059@comcast.net"
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
    
