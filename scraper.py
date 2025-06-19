# scraper.py
import sqlite3
from notifier import send_email_notification, send_desktop_notification

DB_PATH = "data/companies.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_company_urls():
    conn = get_db_connection()
    companies = conn.execute("SELECT name, url, platform FROM companies").fetchall()
    conn.close()
    return companies

def has_seen(job_id):
    conn = get_db_connection()
    result = conn.execute("SELECT 1 FROM seen_jobs WHERE job_id = ?", (job_id,)).fetchone()
    conn.close()
    return result is not None

def mark_seen(job_id):
    conn = get_db_connection()
    conn.execute("INSERT OR IGNORE INTO seen_jobs (job_id) VALUES (?)", (job_id,))
    conn.commit()
    conn.close()

def scrape_jobs():
    new_jobs = []
    companies = fetch_company_urls()

    for company in companies:
        name, url, platform = company["name"], company["url"], company["platform"]

        try:
            if platform == "greenhouse":
                from scrapers.greenhouse_scraper import scrape
            else:
                print(f"[SKIPPED] Unsupported platform '{platform}' for {name}")
                continue

            jobs = scrape(name, url)

            for job in jobs:
                job_id = f"{job['company']}-{job['url']}"
                if has_seen(job_id):
                    continue
                new_jobs.append(job)
                mark_seen(job_id)

        except Exception as e:
            print(f"[ERROR] {name}: {e}")

    return new_jobs

if __name__ == "__main__":
    jobs = scrape_jobs()
    for job in jobs:
        subject = f"[NEW JOB] {job['title']} @ {job['company']}"
        body = f"View job posting: {job['url']}"

        send_desktop_notification(subject, body)
        send_email_notification(subject, body)
