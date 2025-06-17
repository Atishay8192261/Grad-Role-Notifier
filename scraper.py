import requests
from bs4 import BeautifulSoup
import sqlite3
from urllib.parse import urljoin

DB_PATH = "data/companies.db"

# Broad keyword match for new grad/entry-level roles
KEYWORDS = [
    "software engineer", "developer", "test engineer",
    "quality assurance", "graduate", "new grad",
    "entry level", "0-1 years", "0-2 years", "junior",
    "university", "early career"
]

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_company_urls():
    conn = get_db_connection()
    companies = conn.execute("SELECT name, url FROM companies").fetchall()
    conn.close()
    return companies

def is_relevant_job(title):
    title = title.lower()
    return any(keyword in title for keyword in KEYWORDS)

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
    print("[INFO] Starting scrape...")
    companies = fetch_company_urls()
    print(f"[INFO] Found {len(companies)} companies to check.")

    for company in companies:
        name, url = company["name"], company["url"]
        print(f"\n[INFO] Scraping {name}: {url}")
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36"
                )
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"[ERROR] Failed to fetch {url} — Status {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a")
            print(f"[DEBUG] Found {len(links)} links on the page.")

            for link in links:
                title = link.get_text(strip=True)
                href = link.get("href")
                if not title or not href:
                    continue

                print(f"🧷 LINK: {title} — {href}")

                if not is_relevant_job(title):
                    print(f"[SKIP] Not relevant: {title}")
                    continue

                full_url = urljoin(url, href)
                job_id = f"{name}-{full_url}"

                if has_seen(job_id):
                    print(f"[SKIP] Already seen: {title}")
                    continue

                new_jobs.append({
                    "company": name,
                    "title": title,
                    "url": full_url
                })

                print(f"[NEW] Found relevant job: {title} @ {name}")
                mark_seen(job_id)

        except Exception as e:
            print(f"[EXCEPTION] {name}: {e}")
            continue

    return new_jobs

# Manual test runner
if __name__ == "__main__":
    jobs = scrape_jobs()
    print("\n=== SUMMARY ===")
    if not jobs:
        print("No new relevant jobs found.")
    else:
        for job in jobs:
            print(f"[NEW] {job['title']} @ {job['company']} — {job['url']}")
