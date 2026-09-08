"""
Reminder system for JiPudding Desktop Pet
Manages eye care, water, and activity reminders with message pools
"""

from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QDateTime
import random
from config import (
    DEFAULT_EYE_INTERVAL, DEFAULT_WATER_INTERVAL, DEFAULT_ACTIVITY_INTERVAL,
    REMINDER_QUEUE_SPACING, SECONDARY_REMINDER_DELAY,
    EYE_REMINDER_MESSAGES, WATER_REMINDER_MESSAGES, ACTIVITY_REMINDER_MESSAGES
)
from states import PetState

class ReminderType:
    """Reminder type enumeration"""
    EYE = "eye"
    WATER = "water"
    ACTIVITY = "activity"


class ReminderManager(QObject):
    """
    Manages timed reminders with configurable intervals and message pools
    """
    
    # Signals
    reminder_triggered = pyqtSignal(str, str)  # (reminder_type, message)
    reminder_confirmed = pyqtSignal(str)  # (reminder_type)
    reminder_ignored = pyqtSignal(str)  # (reminder_type)
    settings_changed = pyqtSignal(dict)  # New settings
    
    def __init__(self):
        super().__init__()
        
        # Reminder settings
        self.settings = {
            ReminderType.EYE: {
                "enabled": True,
                "interval": DEFAULT_EYE_INTERVAL,
                "timer": QTimer(),
                "next_trigger": 0
            },
            ReminderType.WATER: {
                "enabled": True,
                "interval": DEFAULT_WATER_INTERVAL,
                "timer": QTimer(),
                "next_trigger": 0
            },
            ReminderType.ACTIVITY: {
                "enabled": True,
                "interval": DEFAULT_ACTIVITY_INTERVAL,
                "timer": QTimer(),
                "next_trigger": 0
            }
        }
        
        # Message pools
        self.message_pools = {
            ReminderType.EYE: EYE_REMINDER_MESSAGES,
            ReminderType.WATER: WATER_REMINDER_MESSAGES,
            ReminderType.ACTIVITY: ACTIVITY_REMINDER_MESSAGES
        }
        
        # Reminder queue (to prevent overlapping)
        self.reminder_queue = []
        self.is_showing_reminder = False
        self.queue_timer = QTimer()
        self.queue_timer.timeout.connect(self._process_queue)
        
        # Secondary reminder tracking
        self.pending_secondary_reminders = {}  # {reminder_type: QTimer}
        
        # Setup timers
        self._setup_timers()
        
        # Don't start reminders yet - they'll be started after component wiring
        self.timers_started = False
        self.loading_settings = False
    
    def start_all_reminders(self):
        """Start all enabled reminder timers"""
        if not self.timers_started:
            for reminder_type, config in self.settings.items():
                if config["enabled"]:
                    self._start_reminder_timer(reminder_type)
            self.timers_started = True
    
    def _setup_timers(self):
        """Setup reminder timers"""
        for reminder_type, config in self.settings.items():
            timer = config["timer"]
            timer.setSingleShot(True)
            timer.timeout.connect(lambda rt=reminder_type: self._trigger_reminder(rt))
    
    def _start_reminder_timer(self, reminder_type):
        """
        Start the timer for a specific reminder type
        
        Args:
            reminder_type: Type of reminder (eye, water, activity)
        """
        config = self.settings[reminder_type]
        interval_ms = config["interval"] * 60 * 1000  # Convert minutes to milliseconds
        
        config["timer"].start(interval_ms)
        config["next_trigger"] = QDateTime.currentDateTime().addMSecs(interval_ms)
    
    def _trigger_reminder(self, reminder_type):
        """
        Trigger a reminder
        
        Args:
            reminder_type: Type of reminder to trigger
        """
        if not self.settings[reminder_type]["enabled"]:
            return
        
        # Add to queue
        self.reminder_queue.append(reminder_type)
        
        # Process queue if not already showing a reminder
        if not self.is_showing_reminder:
            self._process_queue()
    
    def _process_queue(self):
        """Process the reminder queue"""
        if not self.reminder_queue or self.is_showing_reminder:
            return
        
        reminder_type = self.reminder_queue.pop(0)
        self._show_reminder(reminder_type)
    
    def _show_reminder(self, reminder_type):
        """
        Show a reminder of the specified type
        
        Args:
            reminder_type: Type of reminder to show
        """
        self.is_showing_reminder = True
        
        # Get random message from pool
        message = self._get_random_message(reminder_type)
        
        # Emit signal
        self.reminder_triggered.emit(reminder_type, message)
        
        # Setup secondary reminder timer
        self._setup_secondary_reminder(reminder_type)
    
    def _get_random_message(self, reminder_type):
        """
        Get a random message from the message pool
        
        Args:
            reminder_type: Type of reminder
            
        Returns:
            Random message string
        """
        messages = self.message_pools.get(reminder_type, [])
        if not messages:
            return "提醒时间到了！"
        
        message = random.choice(messages)
        
        # Format message with interval if needed
        interval = self.settings[reminder_type]["interval"]
        if "{minutes}" in message:
            message = message.format(minutes=interval)
        
        return message
    
    def _setup_secondary_reminder(self, reminder_type):
        """
        Setup a secondary reminder if user doesn't respond
        
        Args:
            reminder_type: Type of reminder
        """
        # Cancel existing secondary reminder for this type
        if reminder_type in self.pending_secondary_reminders:
            self.pending_secondary_reminders[reminder_type].stop()
        
        # Create new secondary reminder timer
        secondary_timer = QTimer()
        secondary_timer.setSingleShot(True)
        secondary_timer.timeout.connect(lambda: self._trigger_secondary_reminder(reminder_type))
        
        # Start timer (5 minutes)
        secondary_timer.start(SECONDARY_REMINDER_DELAY * 1000)
        self.pending_secondary_reminders[reminder_type] = secondary_timer
    
    def _trigger_secondary_reminder(self, reminder_type):
        """
        Trigger a secondary reminder (user didn't respond)
        
        Args:
            reminder_type: Type of reminder
        """
        # Emit ignored signal
        self.reminder_ignored.emit(reminder_type)
        
        # Remove from pending
        if reminder_type in self.pending_secondary_reminders:
            del self.pending_secondary_reminders[reminder_type]
    
    def confirm_reminder(self, reminder_type):
        """
        User confirmed the reminder
        
        Args:
            reminder_type: Type of reminder that was confirmed
        """
        # Cancel secondary reminder
        if reminder_type in self.pending_secondary_reminders:
            self.pending_secondary_reminders[reminder_type].stop()
            del self.pending_secondary_reminders[reminder_type]
        
        # Emit confirmed signal
        self.reminder_confirmed.emit(reminder_type)
        
        # Mark reminder as done
        self.is_showing_reminder = False
        
        # Restart the timer for this reminder type
        if self.settings[reminder_type]["enabled"]:
            self._start_reminder_timer(reminder_type)
        
        # Process next in queue
        QTimer.singleShot(REMINDER_QUEUE_SPACING * 1000, self._process_queue)
    
    def set_reminder_enabled(self, reminder_type, enabled):
        """
        Enable or disable a specific reminder type
        
        Args:
            reminder_type: Type of reminder
            enabled: Whether to enable the reminder
        """
        self.settings[reminder_type]["enabled"] = enabled
        
        if enabled and self.timers_started and not self.loading_settings:
            self._start_reminder_timer(reminder_type)
        else:
            self.settings[reminder_type]["timer"].stop()
        
        # Emit settings changed signal
        self._emit_settings_changed()
    
    def set_reminder_interval(self, reminder_type, interval_minutes):
        """
        Set the interval for a specific reminder type
        
        Args:
            reminder_type: Type of reminder
            interval_minutes: Interval in minutes
        """
        self.settings[reminder_type]["interval"] = interval_minutes
        
        # Restart timer with new interval (only if timers are started and not loading settings)
        if self.settings[reminder_type]["enabled"] and self.timers_started and not self.loading_settings:
            self.settings[reminder_type]["timer"].stop()
            self._start_reminder_timer(reminder_type)
        
        # Emit settings changed signal
        self._emit_settings_changed()
    
    def get_reminder_enabled(self, reminder_type):
        """Check if a reminder type is enabled"""
        return self.settings[reminder_type]["enabled"]
    
    def get_reminder_interval(self, reminder_type):
        """Get the interval for a reminder type"""
        return self.settings[reminder_type]["interval"]
    
    def get_all_settings(self):
        """Get all reminder settings"""
        return {
            "eye_enabled": self.settings[ReminderType.EYE]["enabled"],
            "water_enabled": self.settings[ReminderType.WATER]["enabled"],
            "activity_enabled": self.settings[ReminderType.ACTIVITY]["enabled"],
            "eye_interval": self.settings[ReminderType.EYE]["interval"],
            "water_interval": self.settings[ReminderType.WATER]["interval"],
            "activity_interval": self.settings[ReminderType.ACTIVITY]["interval"]
        }
    
    def load_settings(self, settings):
        """
        Load settings from a dictionary
        
        Args:
            settings: Dictionary with reminder settings
        """
        self.loading_settings = True
        
        if "reminders" in settings:
            reminder_settings = settings["reminders"]
            
            # Load eye settings
            if "eye_enabled" in reminder_settings:
                self.settings[ReminderType.EYE]["enabled"] = reminder_settings["eye_enabled"]
            if "eye_interval" in reminder_settings:
                self.settings[ReminderType.EYE]["interval"] = reminder_settings["eye_interval"]
            
            # Load water settings
            if "water_enabled" in reminder_settings:
                self.settings[ReminderType.WATER]["enabled"] = reminder_settings["water_enabled"]
            if "water_interval" in reminder_settings:
                self.settings[ReminderType.WATER]["interval"] = reminder_settings["water_interval"]
            
            # Load activity settings
            if "activity_enabled" in reminder_settings:
                self.settings[ReminderType.ACTIVITY]["enabled"] = reminder_settings["activity_enabled"]
            if "activity_interval" in reminder_settings:
                self.settings[ReminderType.ACTIVITY]["interval"] = reminder_settings["activity_interval"]
        
        self.loading_settings = False
    
    def _emit_settings_changed(self):
        """Emit settings changed signal"""
        self.settings_changed.emit(self.get_all_settings())
    
    def get_next_reminder_time(self, reminder_type):
        """
        Get the time until next reminder for a type
        
        Args:
            reminder_type: Type of reminder
            
        Returns:
            Remaining time in minutes, or None if disabled
        """
        if not self.settings[reminder_type]["enabled"]:
            return None
        
        remaining_ms = self.settings[reminder_type]["timer"].remainingTime()
        if remaining_ms < 0:
            return None
        
        return remaining_ms / (60 * 1000)  # Convert to minutes
    
    def get_all_next_reminder_times(self):
        """Get next reminder times for all enabled types"""
        times = {}
        for reminder_type in [ReminderType.EYE, ReminderType.WATER, ReminderType.ACTIVITY]:
            time = self.get_next_reminder_time(reminder_type)
            if time is not None:
                times[reminder_type] = time
        return times