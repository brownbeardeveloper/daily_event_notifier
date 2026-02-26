import os
import logging
from dotenv import load_dotenv

from core.config import load_config
from core.file_manager import JsonFileManager
from core.event_manager import EventManager
from core.notification_manager import NotificationManager

load_dotenv()

def main():
  try:
    config = load_config()
    api_key = os.getenv("DISCORD_WEBHOOK_URL")
    file_manager = JsonFileManager(config["file_config"])
    event_manager = EventManager(file_manager)
    notify_manager = NotificationManager(api_key, config["notify_config"])
    events = event_manager.get_todays_events()
    notify_manager.send_notification(events)
  except Exception as e:
    logging.error(e)

if __name__ == "__main__":
  main()