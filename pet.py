"""
Pet window for Jili Desktop Pet
Main window class with transparent background, drag functionality, and position management
"""

from PyQt5.QtCore import Qt, QPoint, QTimer, QRect, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QCursor
from PyQt5.QtWidgets import QWidget, QApplication
from config import PET_WINDOW_SIZE, GRAVITY, BOUNCE_FACTOR, WALK_SPEED
from states import PetState

class PetWindow(QWidget):
    """
    Main pet window with transparent background and drag functionality
    """
    
    # Signals
    clicked = pyqtSignal()
    double_clicked = pyqtSignal()
    drag_started = pyqtSignal()
    drag_ended = pyqtSignal()
    position_changed = pyqtSignal(int, int)
    walking_finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Window setup
        self.setFixedSize(PET_WINDOW_SIZE)
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        # Prevent window from being hidden by system
        self.setAttribute(Qt.WA_QuitOnClose, False)
        
        # Click-through when idle
        # self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setMouseTracking(True)
        
        # Position and movement
        self.start_position = QPoint(0, 0)
        self.drag_position = QPoint(0, 0)
        self.is_dragging = False
        self.is_falling = False
        self.velocity_y = 0
        self.walking_direction = 1  # 1 for right, -1 for left
        self.walking_target = QPoint(0, 0)
        
        # Current sprite
        self.current_pixmap = None
        self.current_frame = 0
        
        # Entry animation
        self.entry_animation_phase = 0
        self.entry_animation_timer = QTimer()
        self.entry_animation_timer.timeout.connect(self._update_entry_animation)
        
        # Physics timer
        self.physics_timer = QTimer()
        self.physics_timer.timeout.connect(self._update_physics)
        
        # Initialize position
        self._initialize_position()
        
        # Show window
        self.show()
        
        # Start entry animation
        self._start_entry_animation()
        # DEBUG: Test if painting works
        from sprite_generator import SpriteGenerator
        sg = SpriteGenerator()
        test_frames = sg.generate_all_sprites()
        from states import PetState
        if test_frames[PetState.IDLE]:
            self.current_pixmap = test_frames[PetState.IDLE][0]
            print(f"DEBUG: pixmap set, size={self.current_pixmap.size()}, isNull={self.current_pixmap.isNull()}")
            self.update()
    
    def _initialize_position(self):
        """Initialize window position at bottom-right of screen"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        
        x = screen_geometry.width() - PET_WINDOW_SIZE.width() - 50
        y = screen_geometry.height() - PET_WINDOW_SIZE.height() - 20
        
        print(f"Setting window position to: ({x}, {y})")
        print(f"Screen size: {screen_geometry.width()}x{screen_geometry.height()}")
        self.move(x, y)
    
    def _start_entry_animation(self):
        """Skip entry animation, just show at bottom"""
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self._initialize_position()
    
    def _update_entry_animation(self):
        """Update entry animation phases"""
        if self.entry_animation_phase == 0:
            # Falling phase
            if self._update_falling():
                # Hit bottom, start bounce
                self.entry_animation_phase = 1
                self.velocity_y = -15  # Bounce up
        elif self.entry_animation_phase == 1:
            # First bounce
            if self._update_falling():
                # Hit bottom again, second bounce
                self.entry_animation_phase = 2
                self.velocity_y = -8  # Smaller bounce
        elif self.entry_animation_phase == 2:
            # Second bounce
            if self._update_falling():
                # Landed, stop animation
                self.entry_animation_phase = 3
                self.entry_animation_timer.stop()
                self.physics_timer.stop()
                self.is_falling = False
                self.velocity_y = 0
                
                # Enable click-through when idle
                self._set_click_through(True)
    
    def _update_falling(self):
        """Update falling physics, return True if hit bottom"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        bottom_y = screen_geometry.height() - PET_WINDOW_SIZE.height() - 20
        
        # Apply gravity
        self.velocity_y += GRAVITY
        new_y = self.y() + int(self.velocity_y)
        
        # Check if hit bottom
        if new_y >= bottom_y:
            self.move(self.x(), bottom_y)
            self.velocity_y = -self.velocity_y * BOUNCE_FACTOR
            
            # Stop if velocity is very low
            if abs(self.velocity_y) < 2:
                self.velocity_y = 0
                return True  # Hit bottom
        else:
            self.move(self.x(), new_y)
        
        return False  # Still falling
    
    def _update_physics(self):
        """Update physics (falling, walking)"""
        if self.is_falling:
            self._update_falling()
        elif self.walking_target != QPoint(0, 0):
            self._update_walking()
    
    def _update_walking(self):
        """Update walking animation"""
        current_pos = self.pos()
        direction = self.walking_target - current_pos
        if direction.manhattanLength() < WALK_SPEED:
            self.move(self.walking_target)
            self.position_changed.emit(self.walking_target.x(), self.walking_target.y())
            self.walking_target = QPoint(0, 0)
            self.physics_timer.stop()
            self.walking_finished.emit()
        else:
            normalized = direction / (direction.manhattanLength() / WALK_SPEED)
            new_pos = current_pos + QPoint(int(normalized.x()), int(normalized.y()))
            self.move(new_pos)
            self.walking_direction = 1 if normalized.x() > 0 else -1
            self.position_changed.emit(new_pos.x(), new_pos.y())
  
    def set_sprite(self, pixmap):
        """Set the current sprite to display"""
        self.current_pixmap = pixmap
        self.update()
    
    def set_click_through(self, enabled):
        """Set whether window is click-through"""
        self._set_click_through(enabled)
    
    def _set_click_through(self, enabled):
        """Disabled - always allow mouse events"""
        pass
    
    def start_drag(self, position):
        """Start dragging the pet"""
        # Stop any walking/physics first
        self.stop_walking()
        self.physics_timer.stop()
        self.is_falling = False
        self.walking_target = QPoint(0, 0)

        self.is_dragging = True
        self.drag_position = position
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.drag_started.emit()

    def update_drag(self, position):
        """Update drag position"""
        if self.is_dragging:
            new_pos = self.mapToGlobal(position) - self.drag_position
            self.move(new_pos)
            self.position_changed.emit(new_pos.x(), new_pos.y())
    
    def end_drag(self):
        """End dragging and start falling"""
        if self.is_dragging:
            self.is_dragging = False
            self.is_falling = True
            self.velocity_y = 0
            self.physics_timer.start(16)
            self.drag_ended.emit()
    
    def start_walking(self, target_x):
        """Start walking to target x position"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        bottom_y = screen_geometry.height() - PET_WINDOW_SIZE.height() - 20
        
        # Clamp target to screen bounds
        target_x = max(0, min(target_x, screen_geometry.width() - PET_WINDOW_SIZE.width()))
        
        self.walking_target = QPoint(target_x, bottom_y)
        self.physics_timer.start(16)
    
    def stop_walking(self):
        """Stop walking"""
        self.walking_target = QPoint(0, 0)
        self.physics_timer.stop()
    
    def jump(self):
        """Make the pet jump"""
        self.velocity_y = -10
        self.is_falling = True
        self.physics_timer.start(16)
    
    def paintEvent(self, event):
        """Paint the current sprite"""
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            if self.current_pixmap:
                # Draw sprite centered
                x = (self.width() - self.current_pixmap.width()) // 2
                y = (self.height() - self.current_pixmap.height()) // 2
                painter.drawPixmap(x, y, self.current_pixmap)
            else:
                print("Warning: current_pixmap is None in paintEvent")
        except Exception as e:
            print(f"PaintEvent error: {e}")
            import traceback
            traceback.print_exc()
    
    def mousePressEvent(self, event):
        """Handle mouse press events"""
        if event.button() == Qt.LeftButton:
            self.start_drag(event.pos())
            self.clicked.emit()
        elif event.button() == Qt.RightButton:
            if hasattr(self, 'interaction_manager') and self.interaction_manager:
                self.interaction_manager.show_context_menu(event.globalPos())
    
    def mouseMoveEvent(self, event):
        """Handle mouse move events"""
        if self.is_dragging:
            self.update_drag(event.pos())
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release events"""
        if event.button() == Qt.LeftButton and self.is_dragging:
            self.end_drag()
    
    def mouseDoubleClickEvent(self, event):
        """Handle double-click events"""
        if event.button() == Qt.LeftButton:
            self.double_clicked.emit()
    
    def enterEvent(self, event):
        """Handle mouse enter"""
        pass

    def leaveEvent(self, event):
        """Handle mouse leave"""
        pass

    def closeEvent(self, event):
        """Handle window close event - prevent accidental closing"""
        print("Pet window close event triggered - ignoring")
        event.ignore()
    
    def show_context_menu(self, global_pos):
        """Show context menu at global position"""
        # This will be connected to interaction manager
        if hasattr(self, 'interaction_manager'):
            self.interaction_manager.show_context_menu(global_pos)
    
    def set_interaction_manager(self, manager):
        """Set the interaction manager"""
        self.interaction_manager = manager
    
    def get_walking_direction(self):
        """Get current walking direction"""
        return self.walking_direction
    
    def is_at_bottom(self):
        """Check if pet is at the bottom of the screen"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        bottom_y = screen_geometry.height() - PET_WINDOW_SIZE.height() - 20
        return self.y() >= bottom_y - 5
