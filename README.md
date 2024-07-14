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
   ```
   git clone https://github.com/Defeeeee/GitBuddy
   cd GitBuddy
   ```

2. **Create and Activate a Virtual Environment (Recommended):**
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   - Create a `.env` file in the project directory.
   - Fill in the following variables with your actual values:
     ```
     URL=your_whatsapp_business_api_url 
     WHATSAPP_ACCESS_TOKEN=your_whatsapp_business_api_token
     PHONE_NUMBER=your_phone_number_with_country_code
     ```
     - You can obtain the `URL` and `WHATSAPP_ACCESS_TOKEN` from your WhatsApp Business API settings.

5. **Schedule with Cron:**
   - Open your crontab: `crontab -e`
   - Add this line, adjusting the path and time as needed:
     ```
     0 16 * * * /path/to/your/virtual/environment/python /path/to/your/script.py 
     ```
     - This example runs the script at 4:00 PM every day.

## Customization

- **Reminder Time:** Change the time in the cron job to when you want the initial reminder.
- **Recurrent Checks:**  Modify `CHECK_INTERVAL_MINUTES` and `MAX_CHECKS` in the script to control how often and how many times the script checks for commits after the initial reminder.
- **GitHub Username:** Update `GITHUB_USERNAME` in the script with your GitHub username.
- **Message Content:** Edit the messages in the `send_whatsapp_message` function to personalize them.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
