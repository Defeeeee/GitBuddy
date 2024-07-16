import os
from datetime import timedelta, timezone

from crontab import CronTab


def get_env_values():
    """Interactively collects environment variable values from the user."""
    env_vars = {
        "URL": "Enter your WhatsApp Cloud API URL: ",
        "WHATSAPP_ACCESS_TOKEN": "Enter your WhatsApp access token: ",
        "PHONE_NUMBER": "Enter your phone number (with country code): ",
        "GITHUB_USERNAME": "Enter your GitHub username: ",
    }
    env_data = {}
    for key, prompt in env_vars.items():
        while True:
            value = input(prompt).strip()
            if value:
                env_data[key] = value
                break
            else:
                print("Value cannot be empty. Please try again.")
    return env_data


def get_cron_schedule():
    """Interactively gets the desired cron schedule from the user."""
    print("\n--- Cron Job Scheduling ---")
    while True:
        schedule_type = input("Choose schedule type (daily, weekly, hourly, or custom): ").lower()
        if schedule_type in ["daily", "weekly", "hourly", "custom"]:
            break
        else:
            print("Invalid schedule type. Please choose from daily, weekly, hourly, or custom.")

    if schedule_type == "daily":
        hour = int(input("Enter hour (0-23) in your local time: "))
        minute = int(input("Enter minute (0-59) in your local time: "))
        return f"{minute} {hour} * * *"

    elif schedule_type == "weekly":
        day = int(input("Enter day of the week (0=Sunday, 1=Monday, etc.): "))
        hour = int(input("Enter hour (0-23) in your local time: "))
        minute = int(input("Enter minute (0-59) in your local time: "))
        return f"{minute} {hour} * * {day}"

    elif schedule_type == "hourly":
        minute = int(input("Enter minute (0-59) in your local time: "))
        return f"{minute} * * * *"

    elif schedule_type == "custom":
        while True:
            custom_schedule = input("Enter custom cron schedule (e.g., '*/30 9-17 * * *'): ")
            try:
                CronTab(custom_schedule)
                return custom_schedule
            except ValueError:
                print("Invalid cron schedule. Please try again.")


def get_user_timezone():
    """Gets the user's timezone offset in the format '+/-HH:MM'."""
    print("\n--- Timezone Setting ---")
    while True:
        try:
            utc_offset_str = input("Enter your UTC timezone offset (e.g., '-03:00', '+05:30'): ")
            offset_hours, offset_minutes = map(int, utc_offset_str.split(':'))
            timezone(timedelta(hours=offset_hours, minutes=offset_minutes))
            return utc_offset_str
        except ValueError:
            print("Invalid timezone format. Please use the format '+/-HH:MM'.")


def configure_gitbuddy():
    """Configures GitBuddy by collecting env values, timezone, and setting up the cron job."""
    print("\n--- GitBuddy Configuration ---")

    env_data = get_env_values()
    cron_schedule = get_cron_schedule()
    user_timezone = get_user_timezone()
    env_data['TIMEZONE'] = user_timezone

    # Write to .env
    with open(".env", "w") as f:
        for key, value in env_data.items():
            f.write(f"{key}={value}\n")

    # Set up cron job (using python-crontab)
    user_cron = CronTab(user=True)
    job = user_cron.new(
        command=f"python {os.path.abspath('main.py')}",
        comment="GitBuddy Commit Reminder"
    )
    job.setall(cron_schedule)
    user_cron.write()

    print("\nConfiguration complete! GitBuddy is ready to remind you about commits.")


if __name__ == "__main__":
    configure_gitbuddy()
