import requests
import os
import time
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Auth0 Management API configuration
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
API_TOKEN = os.getenv('AUTH0_API_TOKEN')

# Slack configuration
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

# File to store previously seen organizations
PREVIOUS_ORGS_FILE = 'previous_orgs.json'

def send_slack_message(message):
    """Send a message to Slack"""
    if not SLACK_WEBHOOK_URL:
        print("Warning: SLACK_WEBHOOK_URL not set. Skipping Slack notification.")
        return
    
    try:
        response = requests.post(
            SLACK_WEBHOOK_URL,
            json={"text": message},
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending Slack message: {e}")

def load_previous_orgs():
    """Load previously seen organizations from file"""
    if os.path.exists(PREVIOUS_ORGS_FILE):
        with open(PREVIOUS_ORGS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_previous_orgs(orgs):
    """Save current organizations to file"""
    with open(PREVIOUS_ORGS_FILE, 'w') as f:
        json.dump(orgs, f)

def get_organizations():
    """Get organizations with sorting by created_at in descending order"""
    url = f"https://{AUTH0_DOMAIN}/api/v2/organizations"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "sort": "created_at:-1"
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_organization_members(org_id):
    """Get members of a specific organization"""
    url = f"https://{AUTH0_DOMAIN}/api/v2/organizations/{org_id}/members"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def find_new_organizations(current_orgs, previous_orgs):
    """Find organizations that weren't in the previous list"""
    previous_ids = {org['id'] for org in previous_orgs}
    return [org for org in current_orgs if org['id'] not in previous_ids]

def format_slack_message(org, members):
    """Format organization details for Slack message"""
    message = [
        f"*New Organization Found!* 🎉",
        f"*Name:* {org['name']}",
        f"*Display Name:* {org['display_name']}",
        f"*ID:* {org['id']}",
        f"*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "\n*Members:*"
    ]
    
    if members:
        for member in members:
            message.append(f"• {member.get('name', 'Unknown')} ({member.get('email', 'No email')})")
    else:
        message.append("No members found")
    
    return "\n".join(message)

def print_organization_details(org):
    """Print details of a single organization"""
    print("\nNew Organization Found!")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"ID: {org['id']}")
    print(f"Name: {org['name']}")
    print(f"Display Name: {org['display_name']}")
    
    # Get and print member information
    try:
        members = get_organization_members(org['id'])
        print("\nMembers:")
        if members:
            for member in members:
                print(f"  - {member.get('name', 'Unknown')} ({member.get('email', 'No email')})")
        else:
            print("  No members found")
        
        # Send to Slack
        slack_message = format_slack_message(org, members)
        send_slack_message(slack_message)
    except Exception as e:
        print(f"  Error fetching members: {e}")
    
    print("-" * 50)

def poll_organizations():
    """Poll for new organizations every minute"""
    print("Starting organization polling system...")
    print("Checking for new organizations every minute")
    print("Press Ctrl+C to stop")
    
    while True:
        try:
            current_orgs = get_organizations()
            previous_orgs = load_previous_orgs()
            
            new_orgs = find_new_organizations(current_orgs, previous_orgs)
            
            if new_orgs:
                print(f"\nFound {len(new_orgs)} new organization(s)!")
                for org in new_orgs:
                    print_organization_details(org)
            else:
                print(f"\nNo new organizations found at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Save current organizations for next comparison
            save_previous_orgs(current_orgs)
            
            # Wait for 1 minute before next check
            print("\nWaiting 1 minute before next check...")
            time.sleep(60)  # 1 minute in seconds
            
        except KeyboardInterrupt:
            print("\nPolling stopped by user")
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            print("Retrying in 5 minutes...")
            time.sleep(5 * 60)  # 5 minutes in seconds

if __name__ == "__main__":
    poll_organizations() 