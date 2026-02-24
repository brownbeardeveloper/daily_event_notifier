from core.config import load_config
from core.file_manager import JsonFileManager
from core.notify_manager import NotifyManager

def main():
  config = load_config()
  file_manager = JsonFileManager(config["file_config"])
  notify_manager = NotifyManager(config["notify_config"])
  events = file_manager.get_all_data()
  notify_manager.send_notification(events)

if __name__ == "__main__":
  main()