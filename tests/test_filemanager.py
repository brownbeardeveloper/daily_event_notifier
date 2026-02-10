from pathlib import Path
from core.file_manager import read_json, write_json
import pytest

class TestFileManager:
  def test_read_json_success(self):
    file_path = Path("tests/test_data/events.json")
    events = read_json(file_path)
    assert events[0]["id"] == 1
    assert events[0]["message"] == "This is the first test message."
    assert events[0]["schedule"] == "once"
    assert events[0]["datetime"] == "2026-02-10T14:25"

  def test_read_json_not_exist(self):
    file_path = Path("this_file_does_not_exist.json")
    with pytest.raises(FileNotFoundError):
      read_json(file_path)

  def test_read_empty_json(self):
    file_path = Path("tests/test_data/empty.json")
    with pytest.raises(ValueError):
      read_json(file_path)