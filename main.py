import os

import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": "Bearer " + os.getenv("WHATSAPP_ACCESS_TOKEN"),
    "Content-Type": "application/json",
}
payload = {
    "messaging_product": "whatsapp",
    "to": os.getenv("PHONE_NUMBER"),  # Recipient's phone number in international format
    "type": "text",
    "text": {
        "body": f"Hello! Today is {datetime.today().strftime('%B %d, %Y')} it's {datetime.now().strftime('%H:%M')}. And you haven't committed to GitHub yet! 🤔",
    }
}

response = requests.post(os.getenv("URL"), headers=headers, json=payload)

if response.status_code == 200:
    print("WhatsApp message sent successfully!")
else:
    print("Error sending message:", response.status_code, response.text)
