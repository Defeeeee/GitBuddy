import os
from datetime import datetime, date
from time import sleep

import requests
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": "Bearer " + os.getenv("WHATSAPP_ACCESS_TOKEN"),
    "Content-Type": "application/json",
}


def send_message(*args):
    if not args:
        message = f"Hello! Today is {datetime.today().strftime('%B %d, %Y')} it's {datetime.now().strftime('%H:%M')}. And you haven't committed to GitHub yet! 🤔"
    else:
        message = args[0]
    payload = {
        "messaging_product": "whatsapp",
        "to": os.getenv("PHONE_NUMBER"),  # Recipient's phone number in international format
        "type": "text",
        "text": {
            "body": message
        }
    }
    response = requests.post(os.getenv("URL"), headers=headers, json=payload)

    if response.status_code == 200:
        print("WhatsApp message sent successfully!")
    else:
        print("Error sending message:", response.status_code, response.text)


def waitAndCheck():
    if not datetime.now().strftime("%H:%M") == "23:00":
        sleep(3600)
        if requests.get(f"https://api.github.com/search/commits?q=author:defeeeee+author-date:{date.today()}").json()[
            "total_count"] == 0:
            send_message()
            waitAndCheck()
        else:
            print("You have already committed today!")
            send_message(f"You have already committed today as of {datetime.now().strftime('%H:%M')}!")
    else:
        sleep(3000)
        if requests.get(f"https://api.github.com/search/commits?q=author:defeeeee+author-date:{date.today()}").json()[
            "total_count"] == 0:
            send_message()
        else:
            print("You have already committed today!")
            send_message(f"You have already committed today as of {datetime.now().strftime('%H:%M')}!")


if __name__ == "__main__":
    if requests.get(f"https://api.github.com/search/commits?q=author:defeeeee+author-date:{date.today()}").json()[
        "total_count"] == 0:
        send_message()
        waitAndCheck()
    else:
        print("You have already committed today!")
        send_message(f"You have already committed today as of {datetime.now().strftime('%H:%M')}!")
