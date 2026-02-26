from datetime import datetime
import requests
from requests.exceptions import RequestException
from core.schemas import BaseEvents, ScheduleType


class NotifyManager:
  def __init__(self, api_key: str, notify_config: dict):
    self.api_key = api_key
    self.title = notify_config['title']
    self.description = notify_config['description']
    self.embed_color = notify_config['color']
    self.error_color = notify_config['error_color']

  def _get_embed_notification(self, events: list[BaseEvents]):
    message = ""
    embed = {
      "title": f"{self.title} - {datetime.now().strftime('%A')}",
      "description": self.description,
      "fields": [],
      "color": self.embed_color
    }

    for event in events:
      if event.schedule == ScheduleType.DAILY:
        time_str = f" at {event.dailytime.strftime('%H:%M')}" if event.dailytime else ""
        message += f"{event.message}{time_str}\n"
      elif event.schedule == ScheduleType.WEEKLY:
        time_str = f" at {event.dailytime.strftime('%H:%M')}" if event.dailytime else ""
        message += f"{event.message}{time_str}\n"
      elif event.schedule == ScheduleType.MONTHLY:
        time_str = f" at {event.dailytime.strftime('%H:%M')}" if event.dailytime else ""
        message += f"{event.message}{time_str}\n"
      elif event.schedule == ScheduleType.ONCE:
        time_str = f" at {event.dailytime.strftime('%H:%M')}" if event.dailytime else ""
        message += f"{event.message}{time_str}\n"

    embed["description"] = message if message else "No events for today."
    return embed

  def _send_message(self, embed: dict) -> int:
    try:
      response = requests.post(
        self.api_key,
        headers={
          "Authorization": f"Bearer {self.api_key}",
          "Content-Type": "application/json"
        },
        json={
          "embeds": [embed]
        }
      )
      return response.status_code
    except RequestException:
      return 0

  def send_notification(self, events: list[BaseEvents]) -> int:
    if not isinstance(events, list) or not events:
      return 0

    embed = self._get_embed_notification(events)
    return self._send_message(embed)
  
  def send_error(self, error: str) -> int:
    return self._send_message({
      "title": "Error",
      "description": error,
      "color": self.error_color
    })
    
    