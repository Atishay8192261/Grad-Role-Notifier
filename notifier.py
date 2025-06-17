import smtplib
import os
from email.message import EmailMessage
from plyer import notification
from dotenv import load_dotenv

# Load env vars
load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# --------------- Desktop Notification ----------------
def send_desktop_notification(title, message):
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=10
        )
        print(f"[DESKTOP] Notified: {title}")
    except Exception as e:
        print(f"[ERROR] Desktop notification failed: {e}")

# --------------- Email Notification ------------------
def send_email_notification(subject, body):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS  # or another recipient
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print(f"[EMAIL] Sent: {subject}")
    except Exception as e:
        print(f"[ERROR] Email failed: {e}")
