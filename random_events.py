"""
Random events and affection system for Jili Desktop Pet
Handles random chat bubbles and affection-based behaviors
"""

from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import random
from config import (
    RANDOM_CHAT_MIN, RANDOM_CHAT_MAX, RANDOM_CHAT_MESSAGES,
    AFFECTION_HIGH, AFFECTION_LOW, AFFECTION_DEFAULT
)
from states import PetState

class RandomEventManager(QObject):
    """
    Manages random events and affection-based behaviors
    """
    
    # Signals
    show_chat_bubble = pyqtSignal(str)  # Show random chat bubble
    # DISABLED to prevent circular dependency
    # affection_changed = pyqtSignal(int)  # Affection score changed
    request_turn_away = pyqtSignal()  # Pet should turn away (low affection)
    
    def __init__(self):
        super().__init__()
        
        # Affection system
        self.affection_score = AFFECTION_DEFAULT
        
        # Random chat timer
        self.chat_timer = QTimer()
        self.chat_timer.timeout.connect(self._trigger_random_chat)
        self.chat_timer.setSingleShot(True)
        
        # Don't start timer yet - it'll be started after component wiring
        self.timer_started = False
    
    def start_timer(self):
        """Start the random chat timer"""
        if not self.timer_started:
            self._schedule_next_chat()
            self.timer_started = True
    
    def set_affection(self, score):
        """
        Set affection score
        
        Args:
            score: New affection score (0-100)
        """
        old_score = self.affection_score
        self.affection_score = max(0, min(100, score))
        
        # Check for affection-based behaviors (no signal to prevent circular dependency)
        if old_score != self.affection_score:
            self._check_affection_behaviors(old_score)
    
    def get_affection(self):
        """Get current affection score"""
        return self.affection_score
    
    def change_affection(self, delta):
        """
        Change affection by a delta amount
        
        Args:
            delta: Amount to change (positive or negative)
        """
        old_score = self.affection_score
        self.affection_score = max(0, min(100, self.affection_score + delta))
        
        # Check for affection-based behaviors (no signal to prevent circular dependency)
        if old_score != self.affection_score:
            self._check_affection_behaviors(old_score)
    
    def _check_affection_behaviors(self, old_score):
        """
        Check and trigger affection-based behaviors
        
        Args:
            old_score: Previous affection score
        """
        # Check if dropped to low affection
        if old_score >= AFFECTION_LOW and self.affection_score < AFFECTION_LOW:
            self.request_turn_away.emit()
        
        # Check if rose to high affection
        if old_score <= AFFECTION_HIGH and self.affection_score > AFFECTION_HIGH:
            # Could trigger special celebration
            pass
    
    def _schedule_next_chat(self):
        """Schedule the next random chat bubble"""
        interval = random.randint(RANDOM_CHAT_MIN, RANDOM_CHAT_MAX) * 1000  # Convert to milliseconds
        self.chat_timer.start(interval)
    
    def _trigger_random_chat(self):
        """Trigger a random chat bubble"""
        # Get random message
        message = random.choice(RANDOM_CHAT_MESSAGES)
        
        # Emit signal to show bubble
        self.show_chat_bubble.emit(message)
        
        # Schedule next chat
        self._schedule_next_chat()
    
    def pause_random_events(self):
        """Pause random events (e.g., during sleep)"""
        self.chat_timer.stop()
    
    def resume_random_events(self):
        """Resume random events"""
        self._schedule_next_chat()
    
    def get_chat_frequency_modifier(self):
        """
        Get chat frequency modifier based on affection
        
        Returns:
            Multiplier for chat frequency (higher = more frequent)
        """
        if self.affection_score > AFFECTION_HIGH:
            return 0.7  # 30% more frequent
        elif self.affection_score < AFFECTION_LOW:
            return 1.5  # 50% less frequent
        else:
            return 1.0  # normal frequency
    
    def should_show_heart_effects(self):
        """
        Check if heart effects should be shown (high affection)
        
        Returns:
            True if heart effects should be shown
        """
        return self.affection_score > AFFECTION_HIGH
    
    def is_turned_away(self):
        """
        Check if pet should be turned away (low affection)
        
        Returns:
            True if pet should be turned away
        """
        return self.affection_score < AFFECTION_LOW
