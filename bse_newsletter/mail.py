import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER = "svno863@gmail.com"
APP_PASSWORD = "ldrzhdcdzajonnuq"

SUBJECT = "BSE Insights: Recent Dividends and Bonuses You Should Know"


# Sends email
def send_email(sender, app_password, recipient, subject, body):
    FROM = sender
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = MIMEMultipart()
    message['From'] = FROM
    message['To'] = ", ".join(TO)
    message['Subject'] = SUBJECT

    message.attach(MIMEText(TEXT, 'html'))

    try:
        print("Sending email...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender,app_password)
        server.sendmail(FROM, TO, message.as_string())
        server.close()
        print('successfully sent the mail')
    except Exception as e:
        print(f"Exception: {e}")
