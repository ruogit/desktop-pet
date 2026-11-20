from PyQt5.QtGui import QPixmap
from states import PetState
from animations import AnimationManager


def test_initial_state_is_none(qapp):
    # Known pitfall: must start as None, otherwise set_state() skips initialization
    assert AnimationManager().current_state is None


def test_frame_count_after_loading(qapp):
    am = AnimationManager()
    am.load_frames(PetState.IDLE, [QPixmap(10, 10) for _ in range(3)])
    assert am.get_frame_count(PetState.IDLE) == 3
    assert am.has_frames(PetState.IDLE)
    assert not am.has_frames(PetState.WALKING)


def test_set_state_switches_when_frames_loaded(qapp):
    am = AnimationManager()
    am.load_frames(PetState.IDLE, [QPixmap(10, 10)])
    am.set_state(PetState.IDLE)
    assert am.current_state == PetState.IDLE