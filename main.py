import os
import logging
from pathlib import Path
from dotenv import load_dotenv

from core.config import load_config
from core.file_manager import JsonFileManager
from core.event_manager import EventManager
from core.notification_manager import NotificationManager

ENV_PATH = Path(__file__).resolve().with_name(".env")
load_dotenv(ENV_PATH)

def main():
  try:
    config = load_config()
    api_key = os.getenv("DISCORD_WEBHOOK_URL")
    if not api_key:
      logging.error("DISCORD_WEBHOOK_URL is not set. Expected it in %s or the process environment.", ENV_PATH)
      return
    file_manager = JsonFileManager(config["file_config"])
    event_manager = EventManager(file_manager)
    notify_manager = NotificationManager(api_key, config["notify_config"])
    events = event_manager.get_todays_events()
    status = notify_manager.send_notification(events)
    if status != 204:
      logging.error("Discord notification was not sent successfully. Status: %s", status)
  except Exception as e:
    logging.exception(e)

if __name__ == "__main__":
  main()
