"""
Animation manager for 吉布丁 Desktop Pet
Handles frame sequencing, timing, and animation loops
"""

from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap
from states import PetState
from config import (
    FRAME_TIMING_FAST, FRAME_TIMING_NORMAL, FRAME_TIMING_SLOW
)

class AnimationManager(QObject):
    """
    Manages animation frame sequencing and timing
    """
    
    # Signals
    frame_ready = pyqtSignal(QPixmap)  # Emit when new frame is ready
    animation_complete = pyqtSignal()  # Emit when animation cycle completes
    
    def __init__(self):
        super().__init__()
        
        # Frame storage
        self.frames = {}  # {PetState: [QPixmap, ...]}
        self.current_frames = []
        self.current_frame_index = 0
        
        # Animation timing
        self.frame_timing = FRAME_TIMING_NORMAL
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._update_frame)
        
        # Direction (for walking)
        self.facing_right = True
        
        # Animation state
        self.is_playing = False
        self.current_state = None
    
    def load_frames(self, state, frame_list):
        """
        Load frames for a specific state
        
        Args:
            state: PetState enum
            frame_list: List of QPixmap frames
        """
        self.frames[state] = frame_list
    
    def set_state(self, state):
        """
        Set the current animation state
        
        Args:
            state: PetState to animate
        """
        if state == self.current_state:
            return
        
        self.current_state = state
        self.current_frame_index = 0
        self.current_frames = self.frames.get(state, [])
        
        # Set timing based on state
        if state in [PetState.WALKING, PetState.EATING]:
            self.frame_timing = FRAME_TIMING_FAST
        elif state in [PetState.SLEEPING]:
            self.frame_timing = FRAME_TIMING_SLOW
        else:
            self.frame_timing = FRAME_TIMING_NORMAL
        
        # Restart timer with new timing
        if self.is_playing:
            self.animation_timer.stop()
            self.animation_timer.start(self.frame_timing)
    
    def start_animation(self):
        """Start the animation loop"""
        if not self.is_playing:
            self.is_playing = True
            self.current_frame_index = 0
            self.animation_timer.start(self.frame_timing)
    
    def stop_animation(self):
        """Stop the animation loop"""
        if self.is_playing:
            self.is_playing = False
            self.animation_timer.stop()
    
    def pause_animation(self):
        """Pause the animation (keep current frame)"""
        if self.is_playing:
            self.is_playing = False
            self.animation_timer.stop()
    
    def resume_animation(self):
        """Resume the animation"""
        if not self.is_playing and self.current_frames:
            self.is_playing = True
            self.animation_timer.start(self.frame_timing)
    
    def _update_frame(self):
        """Update to the next frame"""
        if not self.current_frames:
            return
        
        # Get current frame
        frame = self.current_frames[self.current_frame_index]
        
        # Handle direction flipping for walking
        if self.current_state == PetState.WALKING and not self.facing_right:
            frame = self._flip_frame_horizontally(frame)
        
        # Emit frame
        self.frame_ready.emit(frame)
        
        # Advance to next frame
        self.current_frame_index = (self.current_frame_index + 1) % len(self.current_frames)
        
        # Check if animation completed a full cycle
        if self.current_frame_index == 0:
            self.animation_complete.emit()
    
    def _flip_frame_horizontally(self, pixmap):
        """Flip a pixmap horizontally"""
        return pixmap.transformed(pixmap.transform().scale(-1, 1))
    
    def set_facing_direction(self, facing_right):
        """
        Set the facing direction for walking
        
        Args:
            facing_right: True if facing right, False if facing left
        """
        self.facing_right = facing_right
    
    def get_current_frame(self):
        """Get the current frame without advancing"""
        if self.current_frames and self.current_frame_index < len(self.current_frames):
            frame = self.current_frames[self.current_frame_index]
            
            # Handle direction flipping
            if self.current_state == PetState.WALKING and not self.facing_right:
                frame = self._flip_frame_horizontally(frame)
            
            return frame
        return None
    
    def reset_to_first_frame(self):
        """Reset animation to first frame"""
        self.current_frame_index = 0
        if self.current_frames:
            frame = self.current_frames[0]
            if self.current_state == PetState.WALKING and not self.facing_right:
                frame = self._flip_frame_horizontally(frame)
            self.frame_ready.emit(frame)
    
    def set_frame_timing(self, timing):
        """
        Set custom frame timing
        
        Args:
            timing: Frame timing in milliseconds
        """
        self.frame_timing = timing
        if self.is_playing:
            self.animation_timer.setInterval(timing)
    
    def get_frame_count(self, state):
        """Get the number of frames for a state"""
        return len(self.frames.get(state, []))
    
    def has_frames(self, state):
        """Check if frames are loaded for a state"""
        return state in self.frames and len(self.frames[state]) > 0