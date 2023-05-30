import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

def send_email(receiver_email, subject, message):
    
    # Get the absolute path of the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the relative path to your .env file
    dotenv_path = os.path.join(current_dir, "..", ".env")

    # Load environment variables from the .env file
    load_dotenv(dotenv_path)

    # Email configuration
    sender_email = 'personalcrm0@gmail.com'
    password = os.getenv("GMAIL_PASSWORD") #'loptqelaggqgsluw'

    # Create a MIME message object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message to the MIME object
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Create a secure SSL connection to Gmail's SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

        # Login to your Gmail account
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Close the connection to the SMTP server
        server.quit()