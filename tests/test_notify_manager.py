import pytest, dotenv, os

from core.notify_manager import NotifyManager
from core.schemas import BaseEvents

dotenv.load_dotenv()

class TestNotifyManager:
    """This is a real test, it is better to run it manually"""
    @pytest.fixture
    def notify_config(self):
        return {
            "title": "Test Notification",
            "description": "We are testing the notification system",
            "color": 0x00FF00,
            "error_color": 0xFF0000
        }

    @pytest.fixture
    def events(self):
        return [
            BaseEvents(message="Standup", schedule="daily", dailytime="09:00"),
            BaseEvents(message="Weekly review", schedule="weekly", day_of_week=1),
            BaseEvents(message="Monthly report", schedule="monthly", dd=15),
        ]

    def test_send_real_notification(self, notify_config, events):
        api_key = os.getenv("TEST_WEBHOOK_URL")
        notify_manager = NotifyManager(api_key, notify_config)

        assert api_key is not None
        status = notify_manager.send_notification(events)
        assert status == 204, f"Expected 204, got {status}"

    def test_send_real_error(self, notify_config):
        api_key = os.getenv("TEST_WEBHOOK_URL")
        notify_manager = NotifyManager(api_key, notify_config)

        assert api_key is not None
        status = notify_manager.send_error("Test error")
        assert status == 204, f"Expected 204, got {status}"

    def test_invalid_api_key(self, notify_config, events):
        api_key = "https://discord.com/api/webhooks/invalid/fake_token"
        notify_manager = NotifyManager(api_key, notify_config)
        status = notify_manager.send_notification(events)
        assert status == 400, f"Expected 400 error, got {status}"

    def test_nonexistent_api_key(self, notify_config, events):
        api_key = None
        notify_manager = NotifyManager(api_key, notify_config)
        status = notify_manager.send_notification(events)
        assert status == 0, f"Expected 0 for unreachable URL, got {status}"

    def test_invalid_events(self, notify_config):
        api_key = os.getenv("TEST_WEBHOOK_URL")
        notify_manager = NotifyManager(api_key, notify_config)
        
        assert api_key is not None
        status = notify_manager.send_notification("Invalid events")
        assert status == 0, f"Expected 0 for non-list events, got {status}"
