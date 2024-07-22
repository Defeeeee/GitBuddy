import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

import requests
from crontab import CronTab


def download_files():
    """Downloads main.py and requirements.txt from the GitHub repository."""
    base_url = "https://raw.githubusercontent.com/Defeeeee/GitBuddy/master/"  # Replace with your actual repo URL
    files = ["main.py", "requirements.txt"]
    for file_name in files:
        url = base_url + file_name
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(file_name, "w") as f:
                f.write(response.text)
            print(f"{file_name} downloaded successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {file_name}: {e}")
            exit(1)


def install_dependencies():
    """Installs required dependencies silently from requirements.txt."""
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt", "-q"], check=True)  # -q for quiet mode
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        exit(1)


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
        minute = int(input("Enter minute (0-59) in your local time: ")) - 1
        if minute == -1:
            minute = 59
            hour -= 1
            if hour == -1:
                hour = 23
        return f"{minute} {hour} * * *"

    elif schedule_type == "weekly":
        day = int(input("Enter day of the week (0=Sunday, 1=Monday, etc.): "))
        hour = int(input("Enter hour (0-23) in your local time: "))
        minute = int(input("Enter minute (0-59) in your local time: ")) - 1
        if minute == -1:
            minute = 59
            hour -= 1
            if hour == -1:
                hour = 23
                day = (day - 1) % 7
        return f"{minute} {hour} * * {day}"

    elif schedule_type == "hourly":
        minute = int(input("Enter minute (0-59) in your local time: ")) - 1
        if minute == -1:
            minute = 59
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

            # Additional validation for valid timezones
            datetime.now(user_timezone)  # Test if the timezone is valid

            return user_timezone, utc_offset_str
        except ValueError:
            print("Invalid timezone format or value. Please use the format '+/-HH:MM'.")


def adjust_cron_schedule_to_system_timezone(cron_schedule, user_timezone):
    """Adjusts the cron schedule based on the system's and user's timezones."""
    try:
        system_timezone_str = subprocess.check_output(["date", "+%z"]).decode().strip()
        system_timezone_offset = int(system_timezone_str[:3]) * 60 + int(system_timezone_str[3:])
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"Error getting or parsing system timezone: {e}. Using unadjusted schedule.")
        return cron_schedule

    # Parse the user-provided time
    user_time_str = f"{cron_schedule.split()[1]}:{cron_schedule.split()[0]}"  # HH:MM
    user_datetime = datetime.strptime(user_time_str, "%H:%M").replace(tzinfo=user_timezone)

    # Convert user's time to system time
    system_datetime = user_datetime.astimezone(timezone(timedelta(minutes=system_timezone_offset)))

    # Update the cron schedule with the adjusted hour and minute
    adjusted_schedule = cron_schedule.split()
    adjusted_schedule[1] = str(system_datetime.hour)
    adjusted_schedule[0] = str(system_datetime.minute)
    return " ".join(adjusted_schedule)


def configure_gitbuddy():
    """Configures GitBuddy after confirmation and timezone adjustment."""
    print("\n--- GitBuddy Configuration ---")

    # Check if .env file already exists and handle overwriting
    if os.path.exists(".env"):
        while True:
            overwrite = input(".env file already exists. Overwrite? (yes/no): ").lower()
            if overwrite in ["yes", "y"]:
                break
            elif overwrite in ["no", "n"]:
                print("Configuration aborted. Exiting.")
                return
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    # Download main_script.py and install dependencies
    download_files()
    install_dependencies()

    env_data = get_env_values()
    cron_schedule = get_cron_schedule()
    user_timezone, user_timezone_str = get_user_timezone()

    # Adjust cron schedule to system time
    cron_schedule = adjust_cron_schedule_to_system_timezone(cron_schedule, user_timezone)

    env_data["TIMEZONE"] = user_timezone_str  # Store the timezone in the .env file

    # Write to .env
    with open(".env", "w") as f:
        for key, value in env_data.items():
            f.write(f"{key}={value}\n")

    # Set up cron job (using python-crontab)
    user_cron = CronTab(user=True)
    job = user_cron.new(
        command=f"python3 {os.path.abspath('main.py')}",
        comment="GitBuddy Commit Reminder"
    )
    job.setall(cron_schedule)
    user_cron.write()

    print("\nConfiguration complete! GitBuddy is ready to remind you about commits.")
    print("To view or edit the cron job, run 'crontab -e'.")
    print("To uninstall GitBuddy, simply delete the .env and main.py files.")

    script_dir = os.path.dirname(sys.executable)
    script_path = os.path.join(script_dir, "config")  # Assuming your script is named "config"

    # Schedule self-deletion after a short delay
    subprocess.Popen(f"sleep 5 && rm -rf {script_path} requirements.txt", shell=True)



if __name__ == "__main__":
    configure_gitbuddy()
