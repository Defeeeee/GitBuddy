import os
import random
import requests
from datetime import datetime, date, timezone, timedelta
from dotenv import load_dotenv
import time

load_dotenv()


class GitHubCommitChecker:
    def __init__(self, username):
        self.github_username = username

    def has_commits_today(self):
        # Get today's date and convert to UTC
        today = datetime.now().astimezone(timezone.utc).strftime("%Y-%m-%d")
        url = f"https://api.github.com/search/commits?q=author:{self.github_username} author-date:{today}"

        response = requests.get(url)
        today = date.today()

        if response.status_code == 200:
            commits = response.json()["items"]
            if len(commits) == 0:
                return False

            for commit in commits:
                commit_date = datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%S.%f%z")

                today = datetime.strptime(today, "%Y-%m-%d").date()

                if commit_date.date() == today:
                    return True

            return False
        else:
            print(f"Error checking GitHub commits: {response.status_code} - {response.text}")
            return False


class WhatsAppNotifier:
    def __init__(self, api_url, access_token, phone_number):
        self.api_url = api_url
        self.access_token = access_token
        self.phone_number = phone_number
        self.templates = [
            "not_commited", "nc2", "nc3", "nc4", "nc5", "nc6", "nc7", "nc8", "nc9"
        ]

    def send_message(self, template_name="nc3", params=None):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": self.phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": "en_US"},
            }
        }

        if template_name == "commited":
            payload["template"]["components"] = [{"type": "body"}]
        elif params is not None:
            payload["template"]["components"] = [
                {"type": "body", "parameters": [{"type": "text", "text": params}]}
            ]

        response = requests.post(self.api_url, headers=headers, json=payload)

        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Error sending message: {response.status_code} - {response.text}")


if __name__ == "__main__":
    github_checker = GitHubCommitChecker("defeeeee")
    whatsapp_notifier = WhatsAppNotifier(
        os.getenv("URL"), os.getenv("WHATSAPP_ACCESS_TOKEN"), os.getenv("PHONE_NUMBER")
    )

    check_count = 0
    max_checks = 24
    check_interval_minutes = 30

    while check_count < max_checks:
        if github_checker.has_commits_today():
            whatsapp_notifier.send_message("commited")
            break
        else:
            template = random.choice(whatsapp_notifier.templates)
            whatsapp_notifier.send_message(template, datetime.now().strftime("%H:%M"))
            check_count += 1
            time.sleep(check_interval_minutes * 60)
