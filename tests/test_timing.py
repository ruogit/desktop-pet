import pytest
from timing import minutes_to_ms


def test_45_minutes():
    assert minutes_to_ms(45) == 2_700_000


def test_1_minute():
    assert minutes_to_ms(1) == 60_000


@pytest.mark.parametrize("bad", [0, -1])
def test_rejects_zero_and_negative(bad):
    with pytest.raises(ValueError):
        minutes_to_ms(bad)