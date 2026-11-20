import config


def test_message_pools_not_empty():
    for pool in [config.RANDOM_CHAT_MESSAGES, config.EYE_REMINDER_MESSAGES,
                 config.WATER_REMINDER_MESSAGES, config.ACTIVITY_REMINDER_MESSAGES]:
        assert len(pool) > 0


def test_eye_messages_format_safely():
    # main.py calls .format(minutes=...) on every eye reminder message
    for msg in config.EYE_REMINDER_MESSAGES:
        msg.format(minutes=45)


def test_default_intervals_positive():
    for v in [config.DEFAULT_EYE_INTERVAL, config.DEFAULT_WATER_INTERVAL,
              config.DEFAULT_ACTIVITY_INTERVAL]:
        assert v > 0


def test_random_chat_range_valid():
    assert 0 < config.RANDOM_CHAT_MIN <= config.RANDOM_CHAT_MAX