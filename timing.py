"""Time conversion helpers."""


def minutes_to_ms(minutes):
    """Convert minutes to milliseconds for QTimer."""
    if minutes <= 0:
        raise ValueError("minutes must be positive")
    return int(minutes * 60 * 1000)