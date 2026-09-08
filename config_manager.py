"""
Configuration manager for 吉布丁 Desktop Pet
Handles loading and saving user settings to JSON file
"""

import json
import os
from pathlib import Path
from config import CONFIG_FILE_PATH, DEFAULT_SETTINGS

class ConfigManager:
    """
    Manages configuration persistence to JSON file
    """
    
    def __init__(self):
        self.config_file = Path(CONFIG_FILE_PATH)
        self.settings = DEFAULT_SETTINGS.copy()
        
        # Load existing config if available
        self._load_config()
    
    def _load_config(self):
        """Load configuration from JSON file"""
        if not self.config_file.exists():
            # Create default config
            print("Config file not found, creating default...")
            self._save_config()
            return
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                loaded_settings = json.load(f)
                
                # Merge with defaults (in case new settings were added)
                self._merge_settings(loaded_settings)
                
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config: {e}")
            # Use defaults if load fails
            self.settings = DEFAULT_SETTINGS.copy()
            self._save_config()
    
    def _merge_settings(self, loaded_settings):
        """
        Merge loaded settings with defaults
        
        Args:
            loaded_settings: Settings loaded from file
        """
        # Merge reminder settings
        if "reminders" in loaded_settings:
            for key, value in loaded_settings["reminders"].items():
                if key in self.settings["reminders"]:
                    self.settings["reminders"][key] = value
        
        # Merge affection
        if "affection" in loaded_settings:
            self.settings["affection"] = loaded_settings["affection"]
    
    def _save_config(self):
        """Save configuration to JSON file"""
        try:
            # Ensure directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
                
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def get_settings(self):
        """Get all settings"""
        return self.settings.copy()
    
    def get_reminder_settings(self):
        """Get reminder settings"""
        return self.settings.get("reminders", {}).copy()
    
    def get_affection(self):
        """Get affection score"""
        return self.settings.get("affection", 50)
    
    def set_reminder_enabled(self, reminder_type, enabled):
        """
        Set reminder enabled status
        
        Args:
            reminder_type: Type of reminder (eye, water, activity)
            enabled: Whether the reminder is enabled
        """
        key = f"{reminder_type}_enabled"
        self.settings["reminders"][key] = enabled
        self._save_config()
    
    def set_reminder_interval(self, reminder_type, interval):
        """
        Set reminder interval
        
        Args:
            reminder_type: Type of reminder (eye, water, activity)
            interval: Interval in minutes
        """
        key = f"{reminder_type}_interval"
        self.settings["reminders"][key] = interval
        self._save_config()
    
    def set_affection(self, affection):
        """
        Set affection score
        
        Args:
            affection: Affection score (0-100)
        """
        self.settings["affection"] = max(0, min(100, affection))
        self._save_config()
    
    def update_reminder_settings(self, reminder_settings):
        """
        Update all reminder settings at once
        
        Args:
            reminder_settings: Dictionary of reminder settings
        """
        for key, value in reminder_settings.items():
            if key in self.settings["reminders"]:
                self.settings["reminders"][key] = value
        
        self._save_config()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = DEFAULT_SETTINGS.copy()
        self._save_config()