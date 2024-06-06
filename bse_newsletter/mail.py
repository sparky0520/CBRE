import smtplib

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
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        print("Sending email...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender, app_password)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except Exception as e:
        print(f"Exception: {e}")

# send_email(sender, app_password, sender, "Daily Newsletter", "This is a test email")
