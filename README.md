# Auth0 Organization Monitor

A Python script that monitors Auth0 organizations and sends notifications to Slack when new organizations are created.

## Features

- Monitors Auth0 organizations every minute
- Detects newly created organizations
- Enriches organization data with member information
- Sends notifications to Slack
- Persists organization data between runs

## Setup

1. Clone the repository:
```bash
git clone https://github.com/cdonel707/neworgs.git
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

## Requirements

- Python 3.6+
- requests
- python-dotenv 