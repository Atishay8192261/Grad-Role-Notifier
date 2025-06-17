from notifier import send_email_notification, send_desktop_notification

# Simulate a fake job result
fake_job = {
    "company": "Test Corp",
    "title": "Entry Level Software Engineer",
    "url": "https://example.com/jobs/12345"
}

subject = f"[NEW JOB] {fake_job['title']} @ {fake_job['company']}"
body = f"View job posting: {fake_job['url']}"

# Send both notifications
send_desktop_notification(subject, body)
send_email_notification(subject, body)
