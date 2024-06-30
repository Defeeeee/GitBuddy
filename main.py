import os
import requests
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
import time

load_dotenv()

# Constants (for clarity)
WHATSAPP_API_URL = os.getenv("URL")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
GITHUB_USERNAME = "defeeeee"  # Replace with your actual GitHub username
CHECK_INTERVAL_MINUTES = 15  # Check every 15 minutes after 4 PM
MAX_CHECKS = 24  # Maximum number of checks (15 minutes * 24 = 6 hours)


# Function to send WhatsApp message
def send_whatsapp_message(template_name="not_commited", params=None):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    if template_name == "not_commited" and params is not None:
        payload = {
            "messaging_product": "whatsapp",
            "to": PHONE_NUMBER,
            "type": "template",
            "template": {
                "name": template_name,  # Name of your approved message template
                "language": {"code": "en_US"},
                "components": [
                    {
                        "type": "body",
                        "parameters": [{"type": "text", "text": params}]
                    }
                ]
            }
        }
    elif template_name == "commited":
        payload = {
            "messaging_product": "whatsapp",
            "to": PHONE_NUMBER,
            "type": "template",
            "template": {
                "name": template_name,  # Name of your approved message template
                "language": {"code": "en_US"},
                "components": [
                    {
                        "type": "body",
                    }
                ]
            }
        }
    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        print("WhatsApp message sent successfully!")
        print(response.json())
    else:
        print(f"Error sending message: {response.status_code} - {response.text}")


# Function to check for commits on GitHub
def check_github_commits():
    today = date.today()
    url = f"https://api.github.com/search/commits?q=author:{GITHUB_USERNAME} author-date:{today}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()["total_count"] > 0
    else:
        print(f"Error checking GitHub commits: {response.status_code} - {response.text}")
        return False  # Assume no commits in case of error


# Main logic
if __name__ == "__main__":
    check_count = 0
    while check_count < MAX_CHECKS:  # Only check after 4 PM
        if check_github_commits():
            send_whatsapp_message("commited")
            break  # Stop checking if a commit is found
        else:
            send_whatsapp_message("not_commited", datetime.now().strftime("%H:%M"))
            check_count += 1
            sleep_time = CHECK_INTERVAL_MINUTES * 60  # Convert minutes to seconds
            time.sleep(sleep_time)  # Wait before checking again
