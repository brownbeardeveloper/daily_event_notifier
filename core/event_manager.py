from core.file_manager import JsonFileManager
from core.schemas import BaseEvents


class EventManager:
  def __init__(self, file_manager: JsonFileManager):
    self._file_manager = file_manager

  def get_events(self) -> list[BaseEvents]:
    return self._file_manager.get_all_data()

  def get_event_by_id(self, event_id: int) -> BaseEvents:
    return self._file_manager.get_data_by_id(event_id)

  def add_event(self, event: BaseEvents) -> None:
    self._file_manager.add_new_data(event)

  def update_event(self, event_id: int, event: BaseEvents) -> None:
    self._file_manager.update_data(event_id, event)

  def delete_event(self, event_id: int) -> None:
    self._file_manager.delete_data(event_id)