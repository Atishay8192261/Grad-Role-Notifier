# scrapers/greenhouse_scraper.py
import requests

def scrape(company_name, base_url):
    jobs = []
    try:
        board_token = base_url.rstrip('/').split('/')[-1]
        json_url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"
        response = requests.get(json_url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            for job in data.get("jobs", []):
                title = job["title"]
                job_url = job["absolute_url"]

                jobs.append({
                    "company": company_name,
                    "title": title,
                    "url": job_url
                })
        else:
            print(f"[ERROR] {company_name}: Failed to fetch JSON from Greenhouse")
    except Exception as e:
        print(f"[EXCEPTION] Greenhouse - {company_name}: {e}")

    return jobs
