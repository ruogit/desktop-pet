"""
State machine system for Jili Desktop Pet
Defines pet states and manages state transitions
"""

from enum import Enum
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import random
from config import (
    STATE_DURATION_MIN, STATE_DURATION_MAX, INACTIVITY_TIMEOUT
)

class PetState(Enum):
    """Enumeration of all possible pet states"""
    IDLE = "idle"
    WALKING = "walking"
    DRAGGING = "dragging"
    FALLING = "falling"
    SLEEPING = "sleeping"
    EATING = "eating"
    WAVING = "waving"
    REMINDING = "reminding"


class StateMachine(QObject):
    """
    Manages pet state transitions and timing
    """
    
    # Signals
    state_changed = pyqtSignal(PetState)
    request_animation = pyqtSignal(PetState)
    
    def __init__(self):
        super().__init__()
        self.current_state = PetState.IDLE
        self.previous_state = PetState.IDLE
        
        # Timer for automatic state transitions
        self.state_timer = QTimer()
        self.state_timer.timeout.connect(self._handle_state_timeout)
        
        # Inactivity timer for sleep
        self.inactivity_timer = QTimer()
        self.inactivity_timer.timeout.connect(self._handle_inactivity)
        
        # Flag to prevent automatic transitions during user interaction
        self.user_interacting = False
        
        # Don't start timers yet - they'll be started after component wiring
        self.timers_started = False
    
    def start_timers(self):
        """Start the state machine timers"""
        if not self.timers_started:
            self.state_timer.start(self._get_random_duration())
            self.inactivity_timer.start(INACTIVITY_TIMEOUT)
            self.timers_started = True
        
        # Don't start timers yet - they'll be started after component wiring
        self.timers_started = False
    
    def get_current_state(self):
        """Get the current state"""
        return self.current_state
    
    def set_state(self, new_state, user_initiated=False):
        """
        Set a new state
        
        Args:
            new_state: The new PetState to transition to
            user_initiated: Whether this was triggered by user interaction
        """
        if new_state == self.current_state:
            return
        
        self.previous_state = self.current_state
        self.current_state = new_state
        
        # Emit signals
        self.state_changed.emit(new_state)
        self.request_animation.emit(new_state)
        
        # Handle state-specific logic
        if user_initiated:
            self.user_interacting = True
            self._reset_inactivity_timer()
        else:
            self.user_interacting = False
        
        # Reset state timer for automatic transitions
        if new_state in [PetState.IDLE, PetState.WALKING]:
            self.state_timer.start(self._get_random_duration())
        else:
            self.state_timer.stop()
    
    def force_state(self, new_state):
        """
        Force a state transition (used by external systems like reminders)
        """
        self.set_state(new_state, user_initiated=False)
    
    def return_to_previous_state(self):
        """Return to the previous state"""
        if self.previous_state in [PetState.IDLE, PetState.WALKING]:
            self.set_state(self.previous_state, user_initiated=False)
        else:
            self.set_state(PetState.IDLE, user_initiated=False)
    
    def return_to_idle(self):
        """Return to idle state"""
        self.set_state(PetState.IDLE, user_initiated=False)
    
    def _get_random_duration(self):
        """Get a random duration between min and max"""
        return random.randint(STATE_DURATION_MIN, STATE_DURATION_MAX)
    
    def _handle_state_timeout(self):
        """Handle automatic state transition timeout"""
        if self.user_interacting:
            return  # Don't transition if user is interacting
        
        if self.current_state == PetState.IDLE:
            # Random chance to start walking or stay idle
            if random.random() < 0.6:  # 60% chance to walk
                self.set_state(PetState.WALKING, user_initiated=False)
            else:
                self.state_timer.start(self._get_random_duration())
        elif self.current_state == PetState.WALKING:
            # Return to idle
            self.set_state(PetState.IDLE, user_initiated=False)
    
    def _handle_inactivity(self):
        """Handle inactivity timeout - transition to sleep"""
        if self.current_state not in [PetState.SLEEPING, PetState.DRAGGING, PetState.FALLING]:
            self.set_state(PetState.SLEEPING, user_initiated=False)
    
    def _reset_inactivity_timer(self):
        """Reset the inactivity timer"""
        self.inactivity_timer.stop()
        self.inactivity_timer.start(INACTIVITY_TIMEOUT)
    
    def register_interaction(self):
        """Register a user interaction to prevent automatic transitions"""
        self.user_interacting = True
        self._reset_inactivity_timer()
        
        # Reset user interacting flag after a delay
        QTimer.singleShot(2000, self._clear_user_interacting)
    
    def _clear_user_interacting(self):
        """Clear the user interacting flag"""
        self.user_interacting = False
    
    def can_auto_transition(self):
        """Check if automatic state transitions are allowed"""
        return not self.user_interacting and self.current_state in [PetState.IDLE, PetState.WALKING]
    
    def is_interactive_state(self):
        """Check if current state allows user interaction"""
        return self.current_state not in [PetState.DRAGGING, PetState.FALLING]
