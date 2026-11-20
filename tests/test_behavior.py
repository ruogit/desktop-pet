import pytest
import config
from states import PetState
from behavior import decide_auto_behavior


def test_walk_probability_is_60_percent():
    assert config.WALK_PROBABILITY == 0.6


def test_auto_interval_is_8_seconds():
    assert config.AUTO_BEHAVIOR_INTERVAL_MS == 8000


def test_idle_walks_below_threshold():
    assert decide_auto_behavior(PetState.IDLE, 0.59) == PetState.WALKING


def test_idle_stays_at_or_above_threshold():
    assert decide_auto_behavior(PetState.IDLE, 0.60) is None
    assert decide_auto_behavior(PetState.IDLE, 0.99) is None


@pytest.mark.parametrize("state", [PetState.REMINDING, PetState.WAVING, PetState.EATING])
def test_temporary_states_return_to_idle(state):
    assert decide_auto_behavior(state, 0.5) == PetState.IDLE


@pytest.mark.parametrize("state", [PetState.DRAGGING, PetState.FALLING,
                                   PetState.WALKING, PetState.SLEEPING])
def test_busy_states_not_interrupted(state):
    assert decide_auto_behavior(state, 0.0) is None