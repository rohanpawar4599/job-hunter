import os
import json
import re
import csv
from datetime import datetime
from dotenv import load_dotenv
import requests
import yaml

# Load .env file for local development
load_dotenv()

# Read credentials
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Check if credentials are set
if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
    print("ERROR: Adzuna credentials not found")
    print("Set ADZUNA_APP_ID and ADZUNA_APP_KEY in .env or environment")
    exit(1)

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("ERROR: Telegram credentials not found")
    print("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env or environment")
    exit(1)

print(f"✅ Loaded credentials")
print(f"   Adzuna: {ADZUNA_APP_ID[:5]}...")
print(f"   Telegram: {TELEGRAM_BOT_TOKEN[:10]}...")

# Load config
with open("config.yaml") as f:
    CONFIG = yaml.safe_load(f)

HEADERS = {"User-Agent": "job-hunter/1.0"}

def fetch_adzuna():
    """Fetch jobs from Adzuna"""
    jobs = []
    for keyword in CONFIG["keywords"]:
        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "what": keyword,
            "results_per_page": 50,
            "max_days_old": CONFIG.get("max_days_old", 2)
        }
        try:
            r = requests.get("https://api.adzuna.com/v1/api/jobs/in/search/1", 
                           params=params, headers=HEADERS, timeout=20)
            r.raise_for_status()
            for job in r.json().get("results", []):
                jobs.append({
                    "title": job.get("title", "N/A"),
                    "company": job.get("company", {}).get("display_name", "N/A"),
                    "location": job.get("location", {}).get("display_name", "N/A"),
                    "url": job.get("redirect_url", ""),
                    "source": "Adzuna"
                })
        except Exception as e:
            print(f"Error fetching from Adzuna: {e}")
    return jobs

def send_telegram(message):
    """Send message to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        r = requests.post(url, data=data, timeout=10)
        if r.status_code == 200:
            print("✅ Telegram message sent")
        else:
            print(f"❌ Telegram error: {r.text}")
    except Exception as e:
        print(f"Error sending Telegram: {e}")

def main():
    print(f"[{datetime.now()}] Starting job hunter...")
    
    jobs = fetch_adzuna()
    print(f"Found {len(jobs)} jobs")
    
    if jobs:
        message = f"🚀 Found {len(jobs)} jobs!\n\n"
        for i, job in enumerate(jobs[:10], 1):
            message += f"{i}. <b>{job['title']}</b>\n"
            message += f"   {job['company']} | {job['location']}\n"
            message += f"   {job['source']}\n\n"
        
        send_telegram(message)
    else:
        send_telegram("No new jobs found today")
    
    # Save to CSV
    with open("jobs_report.csv", "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["date", "title", "company", "location", "source"])
        for job in jobs:
            w.writerow({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "source": job["source"]
            })
    
    print("✅ Done!")

if __name__ == "__main__":
    main()