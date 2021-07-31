import smtplib
import csv
import pprint

from .constants import EMAIL_ADDRESS, PASSWORD, SEND_ADDRESS, SMTP_HOST, SMTP_PORT, BODY
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_email(email: list, send_addr: str, body: str):
    msg = MIMEMultipart()
    msg['From'] = send_addr
    msg['To'] = ", ".join([email])
    msg['Cc'] = ", ".join([send_addr])
    msg['Subject'] = "RE: Application for NUS Greyhats"
    msg.attach(MIMEText(body))
    return msg


def send_mail(server, send_addr, to_email, msg):
    try:
        server.sendmail(send_addr, [to_email], msg.as_string())
        print("Mail sent")
    except Exception as e:
        print(f"Error sending mail:{e}")


def generate_receipient_list(filename):
    # Init a list
    lst = []

    # Open the file
    with open(filename, "r") as file:

        # Launch the reader
        reader = csv.reader(file)

        # Remove the header
        next(reader, None)  # skip the headers
        return [(name.strip(), email.strip()) for name, email in reader]


def main():

    recipients = generate_receipient_list("receipients.csv")

    # Print receipients
    pprint.pprint(recipients)
    result = input("Are recipients correct? (y/n): ")

    # Quit if input is not checked
    if result.lower() not in ['y', 'yes']:
        print("Aborted")
        return

    # Create SMTP client
    print("Creating client")
    server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)

    print("Check connection to server")
    print(server.ehlo())
    # Login to zoho
    print("Logging in...")
    print(server.login(EMAIL_ADDRESS, PASSWORD))

    # Iterate through the names
    for name, email in recipients:
        # Create the email
        body = BODY.format(name=name)
        msg = create_email(email, SEND_ADDRESS, body)

        # Send email
        print(f"Sending email to {name}: {email}")
        send_mail(server, SEND_ADDRESS, email, msg)

    # Quit the mail server
    print("Quitting server")
    server.quit()
    print("Connection to server closed")


if __name__ == "__main__":
    main()
