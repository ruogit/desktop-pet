"""
Interaction manager for Jili Desktop Pet
Handles user input, context menus, and affection system
"""

from PyQt5.QtCore import QObject, pyqtSignal, QPoint
from PyQt5.QtWidgets import QMenu, QAction, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtGui import QCursor
from states import PetState
from config import ABOUT_TEXT, AFFECTION_CLICK, AFFECTION_FEEDING

class InteractionManager(QObject):
    """
    Manages user interactions including clicks, context menu, and affection
    """
    
    # Signals
    request_state_change = pyqtSignal(PetState)
    request_jump = pyqtSignal()
    show_about = pyqtSignal()
    open_reminder_settings = pyqtSignal()
    
    def __init__(self, pet_window):
        super().__init__()
        self.pet_window = pet_window
        self.affection_score = 50  # Default affection score
        
        # Connect pet window signals
        pet_window.clicked.connect(self._handle_click)
        pet_window.double_clicked.connect(self._handle_double_click)
        
        # Context menu setup
        self.context_menu = QMenu()
        self._setup_context_menu()
    
    def _setup_context_menu(self):
        """Setup the right-click context menu"""
        # Feed pudding
        feed_action = QAction("🍮 Feed Pudding", self.context_menu)
        feed_action.triggered.connect(self._feed_pet)
        self.context_menu.addAction(feed_action)
        
        # Sleep/Wake
        self.sleep_action = QAction("💤 Sleep", self.context_menu)
        self.sleep_action.triggered.connect(self._toggle_sleep)
        self.context_menu.addAction(self.sleep_action)
        
        # Wave
        wave_action = QAction("👋 Wave", self.context_menu)
        wave_action.triggered.connect(self._wave_pet)
        self.context_menu.addAction(wave_action)
        
        # Separator
        self.context_menu.addSeparator()
        
        # Reminder settings
        reminder_action = QAction("⏰ Reminder Settings", self.context_menu)
        reminder_action.triggered.connect(self._open_reminder_settings)
        self.context_menu.addAction(reminder_action)
        
        # Separator
        self.context_menu.addSeparator()
        
        # About
        about_action = QAction("⭐ About Jili", self.context_menu)
        about_action.triggered.connect(self._show_about)
        self.context_menu.addAction(about_action)
        
        # Exit
        exit_action = QAction("❌ Exit", self.context_menu)
        exit_action.triggered.connect(self._exit_application)
        self.context_menu.addAction(exit_action)
    
    def show_context_menu(self, position):
        """Show the context menu at the given position"""
        # Update sleep action text based on current state
        # This will be handled by the main application
        
        self.context_menu.exec_(position)
    
    def _handle_click(self):
        """Handle single click on pet"""
        # Register interaction with state machine
        # This will be connected in main
        
        # Request jump animation
        self.request_jump.emit()
        
        # Increase affection (handled by main app)
        self.affection_score = max(0, min(100, self.affection_score + AFFECTION_CLICK))
    
    def _handle_double_click(self):
        """Handle double click on pet"""
        # Randomly choose between heart gesture and wave
        import random
        if random.random() < 0.5:
            self.request_state_change.emit(PetState.WAVING)
        else:
            # Could add a heart state here
            self.request_state_change.emit(PetState.WAVING)
        
        # Increase affection (direct, no signal to prevent circular dependency)
        self.affection_score = max(0, min(100, self.affection_score + AFFECTION_CLICK))
    
    def _feed_pet(self):
        """Feed the pet"""
        self.request_state_change.emit(PetState.EATING)
        # Increase affection (direct, no signal to prevent circular dependency)
        self.affection_score = max(0, min(100, self.affection_score + AFFECTION_FEEDING))
    
    def _toggle_sleep(self):
        """Toggle sleep state"""
        # This will be handled by checking current state in main
        self.request_state_change.emit(PetState.SLEEPING)
    
    def _wave_pet(self):
        """Make the pet wave"""
        self.request_state_change.emit(PetState.WAVING)
    
    def _open_reminder_settings(self):
        """Open reminder settings dialog"""
        self.open_reminder_settings.emit()
    
    def _show_about(self):
        """Show about dialog"""
        self.show_about.emit()
    
    def _exit_application(self):
        """Exit the application"""
        from PyQt5.QtWidgets import QApplication
        QApplication.quit()
    
    def _change_affection(self, delta):
        """
        Change affection score
        
        Args:
            delta: Amount to change (positive or negative)
        """
        self.affection_score = max(0, min(100, self.affection_score + delta))
        # Signal disabled to prevent circular dependency
        # self.affection_changed.emit(self.affection_score)
    
    def set_affection(self, score):
        """
        Set affection score directly
        
        Args:
            score: New affection score (0-100)
        """
        self.affection_score = max(0, min(100, score))
        # Signal disabled to prevent circular dependency
        # self.affection_changed.emit(self.affection_score)
    
    def get_affection(self):
        """Get current affection score"""
        return self.affection_score
    
    def save_affection_to_config(self, config_manager):
        """
        Save current affection score to config manager
        
        Args:
            config_manager: ConfigManager instance
        """
        config_manager.set_affection(self.affection_score)
    
    def update_sleep_action_text(self, is_sleeping):
        """Update the sleep action text based on state"""
        if is_sleeping:
            self.sleep_action.setText("☀️ Wake Up")
        else:
            self.sleep_action.setText("💤 Sleep")


class ReminderSettingsDialog(QDialog):
    """
    Dialog for configuring reminder settings
    """
    
    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.current_settings = current_settings.copy()
        self.setWindowTitle("提醒设置")
        self.setFixedSize(300, 250)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout()
        
        # Eye reminder interval
        eye_layout = QHBoxLayout()
        eye_label = QLabel("护眼提醒间隔 (分钟):")
        self.eye_input = QLineEdit(str(self.current_settings.get("eye_interval", 60)))
        eye_layout.addWidget(eye_label)
        eye_layout.addWidget(self.eye_input)
        layout.addLayout(eye_layout)
        
        # Water reminder interval
        water_layout = QHBoxLayout()
        water_label = QLabel("喝水提醒间隔 (分钟):")
        self.water_input = QLineEdit(str(self.current_settings.get("water_interval", 45)))
        water_layout.addWidget(water_label)
        water_layout.addWidget(self.water_input)
        layout.addLayout(water_layout)
        
        # Activity reminder interval
        activity_layout = QHBoxLayout()
        activity_label = QLabel("活动提醒间隔 (分钟):")
        self.activity_input = QLineEdit(str(self.current_settings.get("activity_interval", 90)))
        activity_layout.addWidget(activity_label)
        activity_layout.addWidget(self.activity_input)
        layout.addLayout(activity_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("保存")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_settings(self):
        """Get the updated settings"""
        try:
            return {
                "eye_interval": int(self.eye_input.text()),
                "water_interval": int(self.water_input.text()),
                "activity_interval": int(self.activity_input.text())
            }
        except ValueError:
            # Return original settings if invalid input
            return self.current_settings


class AboutDialog(QDialog):
    """
    About dialog for 吉布丁
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("关于吉布丁")
        self.setFixedSize(350, 200)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout()
        
        # About text
        about_label = QLabel(ABOUT_TEXT)
        about_label.setWordWrap(True)
        about_label.setStyleSheet("QLabel { font-size: 12px; }")
        layout.addWidget(about_label)
        
        # OK button
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        
        self.setLayout(layout)