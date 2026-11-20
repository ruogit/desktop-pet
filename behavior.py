"""Pure decision logic for the pet's automatic behaviour."""
from config import WALK_PROBABILITY
from states import PetState

RETURN_TO_IDLE_STATES = {PetState.REMINDING, PetState.WAVING, PetState.EATING}


def decide_auto_behavior(current, rand_value, walk_probability=WALK_PROBABILITY):
    """
    根据当前状态和一个 0~1 的随机数决定下一个状态。

    Returns:
        需要切换到的 PetState；不需要切换时返回 None
    """
    if current == PetState.IDLE:
        return PetState.WALKING if rand_value < walk_probability else None
    if current in RETURN_TO_IDLE_STATES:
        return PetState.IDLE
    return None