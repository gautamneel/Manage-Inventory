import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server = "smtp.brookfield.com"
port = 25  # For starttls
sender_email = "neelam.gautam@brookfield.com"
receiver_email = "neelam.gautam@brookfield.com"
message = """ """

message = MIMEText(message, "plain")
message["Subject"] = "Gentle reminder"
message["From"] = sender_email

def send_reminder_email(receiver_email, subject, body):
    print('sending emaillllllllllllllll')
    sender_email = "neelam.gautam@brookfield.com"
    server = smtplib.SMTP(smtp_server, port)
    message = """ """

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message.attach(MIMEText(body,'plain'))
    try:
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        # Print any error messages to stdout
        print(f'email sent to {receiver_email}')
    finally:
        server.quit()

