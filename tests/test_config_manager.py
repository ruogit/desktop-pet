import config
import config_manager
from config_manager import ConfigManager


def make_manager(tmp_path, monkeypatch):
    # Use a temp file so your real config file is never touched
    monkeypatch.setattr(config_manager, "CONFIG_FILE_PATH", str(tmp_path / "cfg.json"))
    return ConfigManager()


def test_changing_interval_does_not_mutate_defaults(tmp_path, monkeypatch):
    original = config.DEFAULT_SETTINGS["reminders"]["eye_interval"]
    m = make_manager(tmp_path, monkeypatch)
    m.set_reminder_interval("eye", 999)
    assert config.DEFAULT_SETTINGS["reminders"]["eye_interval"] == original


def test_reset_restores_defaults(tmp_path, monkeypatch):
    m = make_manager(tmp_path, monkeypatch)
    m.set_reminder_interval("eye", 999)
    m.reset_to_defaults()
    assert m.get_reminder_settings()["eye_interval"] == config.DEFAULT_EYE_INTERVAL