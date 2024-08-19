import os
import random
import re
import time
from datetime import datetime, timezone, timedelta

import requests
from dotenv import load_dotenv

"""
Project Name: GitBuddy
Author: Federico Diaz Nemeth

This script checks if a specific GitHub user has made any commits today. If not, it sends a reminder message via WhatsApp.
It uses two main classes: GitHubCommitChecker and WhatsAppNotifier.

GitHubCommitChecker takes a GitHub username and checks if the user has made any commits today using the GitHub API.

WhatsAppNotifier takes an API URL, access token, and phone number, and sends a WhatsApp message using the provided information.

The script runs in a loop, checking for commits at a specified interval and sending a reminder message if no commits have been made.
"""

load_dotenv()

user_timezone_str = os.getenv("TIMEZONE")
offset_hours, offset_minutes = map(int, user_timezone_str.split(':'))
user_timezone = timezone(timedelta(hours=offset_hours, minutes=offset_minutes))


class GitHubCommitChecker:
    def __init__(self, username):
        self.github_username = username

    # Check if the user has made any commits today
    def has_commits_today(self):
        today = datetime.now().astimezone(timezone.utc).strftime("%Y-%m-%d")
        url = f"https://api.github.com/search/commits?q=author:{self.github_username} author-date:{today}"
        response = requests.get(url)

        if response.status_code == 200:
            commits = response.json()["items"]
            if len(commits) == 0:
                return False

            for commit in commits:
                date_str = commit["commit"]["author"]["date"]

                # Remove colon from timezone offset if present
                date_str = re.sub(r"(\d{2}:\d{2})$", lambda x: x.group(1).replace(":", ""), date_str)

                commit_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z")

                today = datetime.now().astimezone(user_timezone).strftime("%Y-%m-%d")
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

    # Send a WhatsApp message
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

    # Create a GitHubCommitChecker object
    github_checker = GitHubCommitChecker(os.getenv("GITHUB_USERNAME"))
    # Create a WhatsAppNotifier object
    whatsapp_notifier = WhatsAppNotifier(
        os.getenv("URL"), os.getenv("WHATSAPP_ACCESS_TOKEN"), os.getenv("PHONE_NUMBER")
    )

    check_interval_minutes = 45

    # Start the loop to check for commits and send reminders
    while datetime.now().astimezone(user_timezone).hour <= 23:
        if github_checker.has_commits_today():
            whatsapp_notifier.send_message("commited")
            break
        else:
            template = random.choice(whatsapp_notifier.templates)
            time_to_send = datetime.now().astimezone(user_timezone) + timedelta(minutes=1)
            whatsapp_notifier.send_message(template, time_to_send.strftime("%H:%M"))
            time.sleep(check_interval_minutes * 60)
