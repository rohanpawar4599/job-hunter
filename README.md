cat > README.md << 'EOF'
# Job Hunter Bot 🤖

Automated job search bot that finds matching DevOps/Cloud roles daily and sends alerts to your phone via Telegram.

## Features

✅ **Daily Job Alerts** - Get job matches every morning at 9 AM IST  
✅ **Smart Filtering** - Filters jobs by your resume keywords (AWS, DevOps, Docker, Kubernetes, etc.)  
✅ **Relevance Scoring** - Scores each job 0-100 based on keyword matches  
✅ **Fresher-Friendly Detection** - Marks roles suitable for freshers/interns  
✅ **CSV Tracking** - Maintains report of all jobs found for reference  
✅ **Zero Manual Work** - Automated via GitHub Actions, runs daily automatically  

## Tech Stack

- **Python 3.11+**
- **GitHub Actions** (CI/CD for daily scheduling)
- **Telegram Bot API** (instant phone alerts)
- **Adzuna API** (job data)
- **Remotive, Greenhouse, Lever** (additional job sources)

## How It Works

1. **Local Testing:**
   ```bash
   git clone https://github.com/rohanpawar4599/job-hunter.git
   cd job-hunter
   pip install -r requirements.txt
   # Create .env with credentials
   python main.py



Automated (GitHub Actions):
Runs daily at 9:00 AM IST
Fetches jobs from multiple sources
Filters by your configured keywords
Scores by relevance to your resume
Sends top matches to your Telegram
Updates CSV report automatically
Setup
Prerequisites
Python 3.8+
GitHub account
Telegram account
Adzuna API credentials (free at adzuna.com/api)




# Clone repo
git clone https://github.com/rohanpawar4599/job-hunter.git
cd job-hunter

# Install dependencies
pip install -r requirements.txt

# Create .env file (DO NOT COMMIT)
cat > .env << 'ENV'
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
ENV

# Test locally
python main.py
