import smtplib
import os
from email.message import EmailMessage
from plyer import notification
from dotenv import load_dotenv
import subprocess
from mailjet_rest import Client

# Load environment variables
load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')  # Not used here, but loaded if needed
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')  # Not used here, but loaded if needed

# --------------- Desktop Notification ----------------
def send_desktop_notification(title, message):
    try:
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script])
    except Exception as e:
        print(f"[ERROR] Desktop notification failed: {e}")

# --------------- Email Notification ------------------
def send_email_notification(subject, body):
    try:
        api_key = os.getenv('MJ_API_KEY')
        api_secret = os.getenv('MJ_API_SECRET')
        sender = os.getenv('MJ_SENDER_EMAIL')  # Should now be "atishayjain@atie.dev"

        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": sender,
                        "Name": "Grad Role Notifier"
                    },
                    "To": [
                        {
                            "Email": "atishayjain8192261@gmail.com",
                            "Name": "Atishay"
                        }
                    ],
                    "Subject": subject,
                    "TextPart": body
                }
            ]
        }
        result = mailjet.send.create(data=data)
        if result.status_code == 200:
            print("[INFO] Mailjet email sent successfully.")
        else:
            print(f"[ERROR] Mailjet failed: {result.status_code} — {result.json()}")

    except Exception as e:
        print(f"[ERROR] Email sending via Mailjet failed: {e}")
