# Auth0 Organization Monitor

A Python script that monitors Auth0 organizations and sends notifications to Slack when new organizations are created.

## Features

- Monitors AuthBan organizations every minute
- Detects newly created organizations
- Enriches organization data with member information
- Sends notifications to Slack
- Persists organization data between runs

## Setup

1. Clone the repository:
```bash
git clone https://github.com/fern-api/neworgs.git
cd neworgs
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your credentials:
```
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_API_TOKEN=your-auth0-api-token
SLACK_WEBHOOK_URL=your-slack-webhook-url
```

## Usage

Run the script:
```bash
python3 get_organizations.py
```

The script will:
- Check for new organizations every minute
- Send notifications to Slack when new organizations are found
- Display information in the console
- Can be stopped with Ctrl+C

## Railway Deployment

1. Create a new project on [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Add the following environment variables in Railway:
   - `AUTH0_DOMAIN`
   - `AUTH0_API_TOKEN`
   - `SLACK_WEBHOOK_URL`
4. Deploy the project

The application will run as a worker process on Railway, continuously monitoring for new organizations.

## Requirements

- Python 3.11+
- requests
- python-dotenv 
