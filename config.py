import os
import subprocess
from crontab import CronTab
from datetime import datetime, timedelta, timezone


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
    """Interactively gets the desired cron schedule from the user in their local time."""
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
            user_timezone = timezone(timedelta(hours=offset_hours, minutes=offset_minutes))
            return user_timezone, utc_offset_str
        except ValueError:
            print("Invalid timezone format. Please use the format '+/-HH:MM'.")


def adjust_cron_schedule_to_system_timezone(cron_schedule, user_timezone):
    """Adjusts the cron schedule based on the system's and user's timezones."""
    try:
        system_timezone_str = subprocess.check_output(["date", "+%z"]).decode().strip()
        system_timezone_offset = int(system_timezone_str[:3]) * 60 + int(system_timezone_str[3:])
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"Error getting or parsing system timezone: {e}. Using unadjusted schedule.")
        return cron_schedule

    # Parse the user-provided time
    user_time_str = f"{cron_schedule.split()[1]}:{cron_schedule.split()[0]}" # HH:MM
    user_datetime = datetime.strptime(user_time_str, "%H:%M").replace(tzinfo=user_timezone)

    # Convert user's time to system time
    system_datetime = user_datetime.astimezone(timezone(timedelta(minutes=system_timezone_offset)))

    # Update the cron schedule with the adjusted hour and minute
    adjusted_schedule = cron_schedule.split()
    adjusted_schedule[1] = str(system_datetime.hour)
    adjusted_schedule[0] = str(system_datetime.minute)
    return " ".join(adjusted_schedule)


def configure_gitbuddy():
    """Configures GitBuddy by collecting env values, timezone, and setting up the cron job."""
    print("\n--- GitBuddy Configuration ---")

    env_data = get_env_values()
    cron_schedule = get_cron_schedule()
    user_timezone, user_timezone_str = get_user_timezone()

    # Adjust cron schedule to system time
    cron_schedule = adjust_cron_schedule_to_system_timezone(cron_schedule, user_timezone)

    env_data['TIMEZONE'] = user_timezone_str  # Store the timezone in the .env file

    # Write to .env
    with open(".env", "w") as f:
        for key, value in env_data.items():
            f.write(f"{key}={value}\n")

    # Set up cron job (using python-crontab)
    user_cron = CronTab(user=True)
    job = user_cron.new(
        command=f"python {os.path.abspath('main_script.py')}",
        comment="GitBuddy Commit Reminder"
    )
    job.setall(cron_schedule)
    user_cron.write()

    print("\nConfiguration complete! GitBuddy is ready to remind you about commits.")


if __name__ == "__main__":
    configure_gitbuddy()
