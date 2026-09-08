"""
System tray icon for 吉布丁 Desktop Pet
Provides tray icon with context menu and tooltip
"""

from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QBrush
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from config import (
    COLOR_TIGER_ORANGE, COLOR_TIGER_STRIPE, COLOR_TIGER_EAR_INNER, COLOR_TIGER_EYE,
    COLOR_STAR_YELLOW
)
from reminders import ReminderType

class TrayIcon(QSystemTrayIcon):
    """
    System tray icon with context menu and dynamic tooltip
    """
    
    def __init__(self, reminder_manager, parent=None):
        super().__init__(parent)
        
        self.reminder_manager = reminder_manager
        self.pet_visible = True
        
        # Generate icon
        self._generate_icon()
        
        # Setup context menu
        self._setup_context_menu()
        
        # Set initial tooltip
        self._update_tooltip()
        
        # Connect signals
        reminder_manager.settings_changed.connect(self._update_tooltip)
        
        # Start tooltip update timer
        self.tooltip_timer = QTimer()
        self.tooltip_timer.timeout.connect(self._update_tooltip)
        self.tooltip_timer.start(30000)  # Update every 30 seconds
    
    def _generate_icon(self):
        """Generate a simplified tiger icon using QPainter"""
        try:
            # Create a 32x32 pixmap
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Draw simplified tiger head
            tiger_color = QColor(COLOR_TIGER_ORANGE)
            painter.setBrush(QBrush(tiger_color))
            painter.setPen(Qt.NoPen)
            
            # Main head (ellipse)
            painter.drawEllipse(8, 8, 16, 16)
            
            # Draw ears
            painter.drawEllipse(6, 4, 8, 8)
            painter.drawEllipse(18, 4, 8, 8)
            
            # Draw inner ears
            ear_inner = QColor(COLOR_TIGER_EAR_INNER)
            painter.setBrush(QBrush(ear_inner))
            painter.drawEllipse(8, 6, 4, 4)
            painter.drawEllipse(20, 6, 4, 4)
            
            # Draw eyes
            eye_color = QColor(COLOR_TIGER_EYE)
            painter.setBrush(QBrush(eye_color))
            painter.drawEllipse(12, 12, 4, 4)
            painter.drawEllipse(16, 12, 4, 4)
            
            # Draw nose
            nose_color = QColor("#FF6B6B")
            painter.setBrush(QBrush(nose_color))
            painter.drawEllipse(14, 16, 4, 3)
            
            # Draw stripes
            stripe_color = QColor(COLOR_TIGER_STRIPE)
            painter.setBrush(QBrush(stripe_color))
            painter.drawEllipse(10, 10, 2, 4)
            painter.drawEllipse(20, 10, 2, 4)
            
            painter.end()
            
            # Create icon from pixmap
            icon = QIcon(pixmap)
            self.setIcon(icon)
        except Exception as e:
            print(f"Error generating tray icon: {e}")
            # Use a simple colored icon as fallback
            from PyQt5.QtGui import QIcon, QPixmap, QColor
            pixmap = QPixmap(32, 32)
            pixmap.fill(QColor(COLOR_TIGER_ORANGE))
            self.setIcon(QIcon(pixmap))
    
    def _draw_small_star(self, painter, x, y, size):
        """Draw a small star shape"""
        from PyQt5.QtGui import QPainterPath
        path = QPainterPath()
        
        # Simple 5-point star
        points = [
            (x, y - size),           # Top
            (x + size * 0.3, y - size * 0.3),
            (x + size, y - size * 0.3),
            (x + size * 0.4, y + size * 0.2),
            (x + size * 0.5, y + size),
            (x, y + size * 0.5),
            (x - size * 0.5, y + size),
            (x - size * 0.4, y + size * 0.2),
            (x - size, y - size * 0.3),
            (x - size * 0.3, y - size * 0.3),
        ]
        
        path.moveTo(points[0][0], points[0][1])
        for point in points[1:]:
            path.lineTo(point[0], point[1])
        path.closeSubpath()
        
        painter.drawPath(path)
    
    def _setup_context_menu(self):
        """Setup the tray icon context menu"""
        menu = QMenu()
        
        # Show/Hide pet
        self.toggle_action = QAction("隐藏吉布丁", menu)
        self.toggle_action.triggered.connect(self._toggle_visibility)
        menu.addAction(self.toggle_action)
        
        menu.addSeparator()
        
        # Eye reminder toggle
        self.eye_action = QAction("护眼提醒: 开", menu)
        self.eye_action.setCheckable(True)
        self.eye_action.setChecked(True)
        self.eye_action.triggered.connect(lambda: self._toggle_reminder(ReminderType.EYE))
        menu.addAction(self.eye_action)
        
        # Water reminder toggle
        self.water_action = QAction("喝水提醒: 开", menu)
        self.water_action.setCheckable(True)
        self.water_action.setChecked(True)
        self.water_action.triggered.connect(lambda: self._toggle_reminder(ReminderType.WATER))
        menu.addAction(self.water_action)
        
        # Activity reminder toggle
        self.activity_action = QAction("活动提醒: 开", menu)
        self.activity_action.setCheckable(True)
        self.activity_action.setChecked(True)
        self.activity_action.triggered.connect(lambda: self._toggle_reminder(ReminderType.ACTIVITY))
        menu.addAction(self.activity_action)
        
        menu.addSeparator()
        
        # Exit
        exit_action = QAction("退出", menu)
        exit_action.triggered.connect(self._exit_application)
        menu.addAction(exit_action)
        
        self.setContextMenu(menu)
    
    def _toggle_visibility(self):
        """Toggle pet visibility"""
        self.pet_visible = not self.pet_visible
        
        if self.pet_visible:
            self.toggle_action.setText("隐藏吉布丁")
            if hasattr(self, 'pet_window'):
                self.pet_window.show()
        else:
            self.toggle_action.setText("显示吉布丁")
            if hasattr(self, 'pet_window'):
                self.pet_window.hide()
    
    def _toggle_reminder(self, reminder_type):
        """Toggle a reminder type"""
        is_enabled = self.reminder_manager.get_reminder_enabled(reminder_type)
        self.reminder_manager.set_reminder_enabled(reminder_type, not is_enabled)
        
        # Update action text
        if reminder_type == ReminderType.EYE:
            self.eye_action.setText(f"护眼提醒: {'开' if not is_enabled else '关'}")
            self.eye_action.setChecked(not is_enabled)
        elif reminder_type == ReminderType.WATER:
            self.water_action.setText(f"喝水提醒: {'开' if not is_enabled else '关'}")
            self.water_action.setChecked(not is_enabled)
        elif reminder_type == ReminderType.ACTIVITY:
            self.activity_action.setText(f"活动提醒: {'开' if not is_enabled else '关'}")
            self.activity_action.setChecked(not is_enabled)
    
    def _update_tooltip(self):
        """Update the tray icon tooltip with next reminder times"""
        tooltip = "吉布丁 🍮"
        
        # Get next reminder times
        times = self.reminder_manager.get_all_next_reminder_times()
        
        if ReminderType.EYE in times:
            eye_time = int(times[ReminderType.EYE])
            tooltip += f" | 下次护眼提醒: 约 {eye_time} 分钟后"
        
        self.setToolTip(tooltip)
    
    def _exit_application(self):
        """Exit the application"""
        from PyQt5.QtWidgets import QApplication
        QApplication.quit()
    
    def set_pet_window(self, pet_window):
        """
        Set reference to pet window for visibility control
        
        Args:
            pet_window: PetWindow instance
        """
        self.pet_window = pet_window
    
    def update_reminder_toggles(self):
        """Update reminder toggle states from settings"""
        self.eye_action.setChecked(self.reminder_manager.get_reminder_enabled(ReminderType.EYE))
        self.water_action.setChecked(self.reminder_manager.get_reminder_enabled(ReminderType.WATER))
        self.activity_action.setChecked(self.reminder_manager.get_reminder_enabled(ReminderType.ACTIVITY))
        
        self.eye_action.setText(f"护眼提醒: {'开' if self.eye_action.isChecked() else '关'}")
        self.water_action.setText(f"喝水提醒: {'开' if self.water_action.isChecked() else '关'}")
        self.activity_action.setText(f"活动提醒: {'开' if self.activity_action.isChecked() else '关'}")