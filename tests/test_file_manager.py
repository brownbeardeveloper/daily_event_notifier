from pathlib import Path
import shutil
import pytest
import datetime

from core.file_manager import JsonFileManager
from core.schemas import BaseEvents


class TestFileManager:
  def test_read_json(self):
    file_config = {"events_file_path": "tests/test_data/events.json"}
    events = JsonFileManager(file_config).get_all_data()
    
    assert isinstance(events, list)
    assert len(events) > 0
    assert isinstance(events[0], BaseEvents)

  def test_read_blank_json(self):
    file_config = {"events_file_path": "tests/test_data/blank.json"}
    events = JsonFileManager(file_config).get_all_data()

    assert isinstance(events, list)
    assert len(events) == 0
    with pytest.raises(IndexError):
      events[0]

  def test_read_json_not_exist(self, tmp_path):
    dst = tmp_path / "new_events.json"
    file_config = {"events_file_path": str(dst)}
    events = JsonFileManager(file_config).get_all_data()

    assert isinstance(events, list)
    assert len(events) == 0
    assert dst.exists()

  def test_read_empty_json(self):
    file_config = {"events_file_path": "tests/test_data/empty.json"}
    with pytest.raises(ValueError):
      JsonFileManager(file_config).get_all_data()

  def test_read_invalid_json(self):
    file_config = {"events_file_path": "tests/test_data/invalid.json"}
    with pytest.raises(ValueError):
      JsonFileManager(file_config).get_all_data()

  def test_write_json(self, tmp_path):
    src = Path("tests/test_data/events.json")
    dst = tmp_path / "events.json"
    shutil.copy(src, dst) # copy test data to temp directory

    fileManager = JsonFileManager({"events_file_path": str(dst)})
    events_before = fileManager.get_all_data()
    new_event = BaseEvents(message="Test", schedule="daily", dailytime="12:00")
    fileManager.add_new_data(new_event)
    events_after = fileManager.get_all_data()

    assert len(events_after) == len(events_before) + 1
    assert events_after[-1].message == new_event.message 
    assert events_after[-1].schedule == new_event.schedule
    assert events_after[-1].dailytime == new_event.dailytime

  def test_write_json_not_exist(self, tmp_path):
    dst = tmp_path / "new_events.json"
    file_config = {"events_file_path": str(dst)}
    fm = JsonFileManager(file_config)
    fm.add_new_data(BaseEvents(message="Test", schedule="daily", dailytime="12:00"))
    events = fm.get_all_data()
    assert len(events) == 1
    assert events[0].message == "Test"

  def test_update_json(self, tmp_path):
    id_1, idx = 1, 0
    src = Path("tests/test_data/events.json")
    dst = tmp_path / "events.json"
    shutil.copy(src, dst) # copy test data to temp directory

    fileManager = JsonFileManager({"events_file_path": str(dst)})
    events_before = fileManager.get_all_data()
    fileManager.update_data(
      key=id_1,
      value=BaseEvents(message="Updated", schedule="once", date="2026-02-15T12:00:00")
    )
    events_after = fileManager.get_all_data()
    updated_event = fileManager.get_data_by_id(id_1)

    assert len(events_after) == len(events_before)
    assert updated_event.id == id_1
    assert events_before[idx].message == "Test event"
    assert events_before[idx].schedule.value == "daily"
    assert events_before[idx].dailytime == datetime.time(12, 0) 
    assert updated_event.message == "Updated"
    assert updated_event.schedule.value == "once"
    assert updated_event.date == datetime.datetime(2026, 2, 15, 12, 0)

  def test_delete_json(self, tmp_path):
    id_1 = 1
    src = Path("tests/test_data/events.json")
    dst = tmp_path / "events.json"
    shutil.copy(src, dst) # copy test data to temp directory

    fileManager = JsonFileManager({"events_file_path": str(dst)})
    events_before = fileManager.get_all_data()
    fileManager.delete_data(id_1)
    events_after = fileManager.get_all_data()

    assert len(events_after) == len(events_before) - 1
    assert events_after == []