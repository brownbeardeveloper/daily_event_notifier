import json
import pytest
from core.file_manager import JsonFileManager
from core.event_manager import EventManager
from core.schemas import BaseEvents, ScheduleType
from datetime import time


def _create_file_manager(tmp_path, events: list[dict]) -> JsonFileManager:
  """Helper: writes events to a tmp JSON file and returns a real JsonFileManager."""
  file_path = tmp_path / "events.json"
  file_path.write_text(json.dumps(events))
  return JsonFileManager({"events_file_path": str(file_path)})


class TestEventManager:
  SAMPLE_EVENTS = [
    {"id": 0, "message": "Stand-up", "schedule": "daily", "time": "09:00:00"},
    {"id": 1, "message": "Lunch", "schedule": "daily", "time": "12:00:00"},
  ]

  def _create_event_manager(self, tmp_path, events: list[dict] | None = None) -> EventManager:
    """Helper: creates an EventManager backed by a tmp JSON file."""
    data = self.SAMPLE_EVENTS if events is None else events
    fm = _create_file_manager(tmp_path, data)
    return EventManager(fm)

  def test_get_events_returns_all_events(self, tmp_path):
    em = self._create_event_manager(tmp_path)
    result = em.get_events()
    assert len(result) == 2
    assert result[0].message == "Stand-up"
    assert result[1].message == "Lunch"

  def test_get_events_returns_empty_list_when_no_events(self, tmp_path):
    em = self._create_event_manager(tmp_path, [])
    result = em.get_events()
    assert result == []

  def test_get_event_by_id(self, tmp_path):
    em = self._create_event_manager(tmp_path)
    result = em.get_event_by_id(1)
    assert result.id == 1
    assert result.message == "Lunch"

  def test_get_event_by_id_not_found(self, tmp_path):
    em = self._create_event_manager(tmp_path, [])
    with pytest.raises(KeyError):
      em.get_event_by_id(99)

  def test_add_event(self, tmp_path):
    em = self._create_event_manager(tmp_path, [])
    event = BaseEvents(message="Meeting", schedule=ScheduleType.DAILY, time=time(14, 0))
    em.add_event(event)

    events = em.get_events()
    assert len(events) == 1
    assert events[0].message == "Meeting"
    assert events[0].id == 0

  def test_update_event(self, tmp_path):
    em = self._create_event_manager(tmp_path, [self.SAMPLE_EVENTS[0]])
    updated = BaseEvents(message="Standup v2", schedule=ScheduleType.DAILY, time=time(10, 0))
    em.update_event(0, updated)

    result = em.get_event_by_id(0)
    assert result.message == "Standup v2"
    assert result.time == time(10, 0)

  def test_delete_event(self, tmp_path):
    em = self._create_event_manager(tmp_path)
    em.delete_event(0)

    events = em.get_events()
    assert len(events) == 1
    assert events[0].id == 1

  def test_delete_event_not_found(self, tmp_path):
    em = self._create_event_manager(tmp_path, [])
    with pytest.raises(KeyError):
      em.delete_event(99)