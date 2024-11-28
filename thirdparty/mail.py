import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configuration.get_config import config

mail_config = config("mail_config")
def send_email(to_email, message, subject = "Reminder From Intellitask"):
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    sender_email = mail_config["mail_id"]
    app_password = mail_config["password"]
    
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls() 
        server.login(sender_email, app_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        print("Email sent successfully!")
