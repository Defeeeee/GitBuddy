<img src="https://github.com/user-attachments/assets/b8a0a00f-951f-48ee-b198-a5224a244562" width="300">
<br>

GitBuddy is a simple yet handy script that reminds you to make your daily GitHub commits. If you haven't committed by a specified time each day, it sends you a friendly WhatsApp message as a nudge.

## Features

- **Daily Reminders:** Customizable to send reminders at a time of your choosing.
- **Recurrent Checks:** Optionally checks multiple times after the initial reminder in case you forget.
- **Customizable:** Easily adapt the reminder frequency, GitHub username, and message content.
- **WhatsApp Integration:** Leverages the WhatsApp Business API for convenient notifications.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Defeeeee/GitBuddy](https://github.com/Defeeeee/GitBuddy)
   cd GitBuddy
   ```

2. **Create and Activate a Virtual Environment (Recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate 
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Configuration Script:**
   ```bash
   python config.py
   ```
   - The script will guide you through setting up:
      - Your WhatsApp Business API credentials (`URL`, `WHATSAPP_ACCESS_TOKEN`)
      - Your phone number (`PHONE_NUMBER`)
      - Your GitHub username (`GITHUB_USERNAME`)
      - Your desired reminder schedule (time, frequency, etc.)
      - Your timezone (to ensure accurate scheduling)

## Customization

- **Message Content:** Edit the messages in the `send_whatsapp_message` function within `main.py` to personalize them.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
