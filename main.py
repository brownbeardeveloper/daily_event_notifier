import os
import logging
from dotenv import load_dotenv

from core.config import load_config
from core.file_manager import JsonFileManager
from core.notify_manager import NotifyManager

load_dotenv()

def main():
  try:
    config = load_config()
    api_key = os.getenv("DISCORD_WEBHOOK_URL")
    file_manager = JsonFileManager(config["file_config"])
    notify_manager = NotifyManager(api_key, config["notify_config"])
    events = file_manager.get_all_data()
    notify_manager.send_notification(events)
  except Exception as e:
    logging.error(e)

if __name__ == "__main__":
  main()