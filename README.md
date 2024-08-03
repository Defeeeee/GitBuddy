<img src="https://github.com/user-attachments/assets/b8a0a00f-951f-48ee-b198-a5224a244562" width="300">
<br>

GitBuddy is a simple yet handy script that reminds you to make your daily GitHub commits. If you haven't committed by a specified time each day, it sends you a friendly WhatsApp message as a nudge.

## Features

- **Daily Reminders:** Customizable to send reminders at a time of your choosing.
- **Recurrent Checks:** Optionally checks multiple times after the initial reminder in case you forget.
- **Customizable:** Easily adapt the reminder frequency, GitHub username, and message content.
- **WhatsApp Integration:** Leverages the WhatsApp Business API for convenient notifications.

## Installation

1. **Download and uncompress the current version installer**
   ```bash
   wget https://github.com/Defeeeee/GitBuddy/releases/download/2.1.2/GitBuddy-2.1.2.tgz
   tar -xvzf GitBuddy-2.1.2.tgz
   cd GitBuddy-2.1.2
   ```

2. **Run config executable and follow the instructions:**
   ```bash
   ./config
   ```
   - The script will fetch the files from the repo and install dependencies
   - The script will also guide you through setting up:
      - Your WhatsApp Business API credentials (`URL`, `WHATSAPP_ACCESS_TOKEN`)
      - Your phone number (`PHONE_NUMBER`)
      - Your GitHub username (`GITHUB_USERNAME`)
      - Your desired reminder schedule (time, frequency, etc.)
      - Your timezone (to ensure accurate scheduling)

## Customization

- **Message Content:** Edit the messages in the `send_whatsapp_message` function within `main.py` to personalize them.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
