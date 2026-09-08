"""
Chat Bubble for Jili Desktop Pet
Displays text bubbles above the pet
"""

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty, QRectF
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QFont, QPen
from config import COLOR_BUBBLE_BG, COLOR_BUBBLE_BORDER, COLOR_TEXT_DARK, SMALL_BUBBLE_DURATION, BUBBLE_FADE_IN


class ChatBubble(QWidget):
    """A chat bubble widget that displays text above the pet"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        self.text = ""
        self._opacity = 0.0
        
        # Auto-dismiss timer
        self.dismiss_timer = QTimer()
        self.dismiss_timer.timeout.connect(self.hide)
        
        # Fade animation
        self.fade_animation = QPropertyAnimation(self, b"opacity")
        self.fade_animation.setDuration(BUBBLE_FADE_IN)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        
    def set_opacity(self, value):
        """Set opacity for animation"""
        self._opacity = value
        self.update()
        
    def get_opacity(self):
        """Get current opacity"""
        return self._opacity
    
    opacity = pyqtProperty(float, get_opacity, set_opacity)
    
    def show_message(self, text, duration=SMALL_BUBBLE_DURATION):
        """Show a message in the bubble"""
        self.text = text
        self._opacity = 0.0
        
        # Calculate size based on text
        self.calculate_size()
        
        # Show and fade in
        self.show()
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()
        
        # Auto-dismiss
        self.dismiss_timer.start(duration)
    
    def calculate_size(self):
        """Calculate bubble size based on text"""
        # Create a temporary label to measure text
        temp_label = QLabel(self.text)
        temp_label.setFont(QFont("Arial", 10))
        temp_label.adjustSize()
        
        text_width = temp_label.width()
        text_height = temp_label.height()
        
        # Add padding
        padding = 20
        self.setFixedSize(text_width + padding * 2, text_height + padding * 2 + 15)  # +15 for arrow
    
    def paintEvent(self, event):
        """Paint the bubble"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set opacity
        painter.setOpacity(self._opacity)
        
        # Draw bubble background
        path = QPainterPath()
        rect = self.rect()
        
        # Rounded rectangle
        radius = 10
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height() - 15), radius, radius)
        
        # Draw arrow at bottom
        arrow_width = 15
        arrow_height = 15
        center_x = rect.width() / 2
        arrow_x = center_x - arrow_width / 2
        arrow_y = rect.height() - 15
        
        path.moveTo(arrow_x, arrow_y)
        path.lineTo(center_x, rect.height())
        path.lineTo(arrow_x + arrow_width, arrow_y)
        
        # Fill background
        painter.setBrush(QColor(COLOR_BUBBLE_BG))
        painter.setPen(QPen(QColor(COLOR_BUBBLE_BORDER), 2))
        painter.drawPath(path)
        
        # Draw text
        painter.setPen(QColor(COLOR_TEXT_DARK))
        painter.setFont(QFont("Arial", 10))
        
        text_rect = QRectF(10, 10, rect.width() - 20, rect.height() - 35)
        painter.drawText(text_rect, Qt.AlignCenter, self.text)
    
    def hide(self):
        """Hide the bubble"""
        self.dismiss_timer.stop()
        try:
            self.fade_animation.finished.disconnect()
        except:
            pass
        self._opacity = 0.0
        self.update()
        super().hide()
    
    def position_above_pet(self, pet_window):
        """Position the bubble above the pet window"""
        if not pet_window.isVisible():
            return
        
        pet_rect = pet_window.geometry()
        bubble_rect = self.geometry()
        
        # Position above pet
        x = pet_rect.x() + (pet_rect.width() - bubble_rect.width()) // 2
        y = pet_rect.y() - bubble_rect.height() + 10
        
        # Ensure bubble stays within screen
        screen = pet_window.screen().availableGeometry()
        
        if x < screen.left():
            x = screen.left()
        elif x + bubble_rect.width() > screen.right():
            x = screen.right() - bubble_rect.width()
        
        if y < screen.top():
            y = screen.top()
        
        self.move(x, y)
