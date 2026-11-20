import re
from pathlib import Path

MAIN = Path(__file__).resolve().parent.parent / "main.py"


def test_reminder_timers_use_minutes_to_ms():
    """Regression: reminder intervals are in minutes but QTimer needs milliseconds."""
    source = MAIN.read_text(encoding="utf-8")
    bad = re.findall(r"_timer\.start\(self\.\w+_interval\)", source)
    assert not bad, f"Reminder timer started without minutes_to_ms(): {bad}"


def test_auto_timer_uses_constant():
    source = MAIN.read_text(encoding="utf-8")
    assert "auto_timer.start(6000)" not in source
    assert "auto_timer.start(8000)" not in source