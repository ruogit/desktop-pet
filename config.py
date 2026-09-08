"""
Configuration file for Jili Desktop Pet
Contains all color constants, size settings, animation timings, and default values
"""

from PyQt5.QtCore import QSize
import os
from pathlib import Path

# =============================================================================
# COLOR CONSTANTS
# =============================================================================

# Main colors - Cute Tiger Theme
COLOR_TIGER_ORANGE = "#FFB366"      # Cute orange for tiger body
COLOR_TIGER_WHITE = "#FFF5E6"       # White for belly and face
COLOR_TIGER_STRIPE = "#8B4513"     # Soft brown stripes
COLOR_TIGER_NOSE = "#FF6B6B"       # Cute pink nose
COLOR_TIGER_EAR_INNER = "#FFB6C1"  # Pink ear inner
COLOR_TIGER_EYE = "#4A4A4A"        # Dark gray eyes
COLOR_TIGER_EYE_HIGHLIGHT = "#FFFFFF"  # White eye highlight
COLOR_TIGER_WHISKER = "#8B4513"    # Brown whiskers
COLOR_TIGER_BLUSH = "#FFB6C1"      # Pink blush
COLOR_STAR_YELLOW = "#FFD700"      # Star highlights
COLOR_BUBBLE_BG = "#FFF5E6"         # Light cream bubble background
COLOR_BUBBLE_BORDER = "#FFB366"    # Tiger orange bubble border
COLOR_TEXT_DARK = "#8B4513"         # Brown text color

# Additional colors
COLOR_WHITE = "#FFFFFF"
COLOR_BLACK = "#000000"
COLOR_LIGHT_ORANGE = "#FFCC80"
COLOR_DARK_STRIPE = "#6B3510"

# =============================================================================
# SIZE CONSTANTS
# =============================================================================

# Window sizes
PET_WINDOW_SIZE = QSize(200, 200)  # Increased from 100x100 for better detail
PET_DISPLAY_SIZE = 200  # Display size in pixels
SPRITE_SIZE = 256       # Increased from 128 for better detail

# Animation frame sizes
FRAME_COUNT_IDLE = 6
FRAME_COUNT_WALKING = 8
FRAME_COUNT_DRAGGING = 4
FRAME_COUNT_FALLING = 4
FRAME_COUNT_SLEEPING = 4
FRAME_COUNT_EATING = 6
FRAME_COUNT_WAVING = 6
FRAME_COUNT_REMINDING = 6

# =============================================================================
# ANIMATION TIMING
# =============================================================================

# Frame timing (milliseconds)
FRAME_TIMING_FAST = 100      # Fast animations
FRAME_TIMING_NORMAL = 150    # Normal animations
FRAME_TIMING_SLOW = 200      # Slow animations

# State durations (milliseconds)
STATE_DURATION_MIN = 5000    # Minimum state duration
STATE_DURATION_MAX = 15000  # Maximum state duration
INACTIVITY_TIMEOUT = 30000  # 30 seconds of inactivity before sleep
BUBBLE_FADE_IN = 200        # Bubble fade-in duration
SMALL_BUBBLE_DURATION = 10000 # Small bubble auto-dismiss

# =============================================================================
# REMINDER SETTINGS
# =============================================================================

# Default reminder intervals (in minutes)
DEFAULT_EYE_INTERVAL = 45
DEFAULT_WATER_INTERVAL = 30
DEFAULT_ACTIVITY_INTERVAL = 60

# Reminder queue spacing (seconds)
REMINDER_QUEUE_SPACING = 30

# Secondary reminder delay (seconds)
SECONDARY_REMINDER_DELAY = 300  # 5 minutes

# =============================================================================
# RANDOM EVENT SETTINGS
# =============================================================================

# Random chat bubble interval (seconds)
RANDOM_CHAT_MIN = 180  # 3 minutes
RANDOM_CHAT_MAX = 480  # 8 minutes

# =============================================================================
# AFFECTION SYSTEM
# =============================================================================

# Affection score range
AFFECTION_MIN = 0
AFFECTION_MAX = 100
AFFECTION_DEFAULT = 50

# Affection thresholds
AFFECTION_HIGH = 80    # High affection threshold
AFFECTION_LOW = 30     # Low affection threshold

# Affection changes
AFFECTION_CLICK = 2
AFFECTION_REMINDER_RESPONSE = 3
AFFECTION_FEEDING = 5
AFFECTION_IGNORE_REMINDER = -1

# =============================================================================
# PHYSICS AND MOVEMENT
# =============================================================================

# Walking speed
WALK_SPEED = 2  # Pixels per frame

# Gravity
GRAVITY = 0.5   # Pixels per frame squared
BOUNCE_FACTOR = 0.6  # Energy retained after bounce

# =============================================================================
# CONFIG FILE PATH
# =============================================================================

def get_config_path():
    """Get the path to the config file"""
    home_dir = Path.home()
    return home_dir / ".jili_config.json"

CONFIG_FILE_PATH = str(get_config_path())

# =============================================================================
# DEFAULT SETTINGS
# =============================================================================

DEFAULT_SETTINGS = {
    "reminders": {
        "eye_enabled": True,
        "water_enabled": True,
        "activity_enabled": True,
        "eye_interval": DEFAULT_EYE_INTERVAL,
        "water_interval": DEFAULT_WATER_INTERVAL,
        "activity_interval": DEFAULT_ACTIVITY_INTERVAL
    },
    "affection": AFFECTION_DEFAULT
}

# =============================================================================
# REMINDER MESSAGE POOLS
# =============================================================================

EYE_REMINDER_MESSAGES = [
    "👀 Time to rest your eyes! Look at something far away for a bit~ 🍀",
    "👀 Hey! Let your eyes relax~ Look out the window 🌿",
    "👀 Jili reminds you: Your eyes are precious! Take a break~ ⭐",
    "👀 You've been staring at the screen too long! Close your eyes for 10 seconds~ 💤",
    "👀 {minutes} minutes passed! Blink a few times and look at the distance~ ✨"
]

WATER_REMINDER_MESSAGES = [
    "💧 Time to drink water~ Stay hydrated, 8 cups a day! 🐯",
    "💧 Glug glug~ Jili wants water too! Have a glass with me 🥛",
    "💧 Water is life! Come, have a drink with Jili~ 🐯",
    "💧 Water time! How many cups have you had today? 🥂"
]

ACTIVITY_REMINDER_MESSAGES = [
    "🧍 You've been sitting too long! Stand up and stretch~ ✨",
    "🧍 Move your body a bit! Jili will do stretches with you~ 💪",
    "🧍 Sitting too long is bad! Take a walk, look outside~ Jili will be here waiting! ⭐",
    "🧍 Stand up! Move around! Stretch your neck and waist~ A healthy body means a happy day 🍮"
]

# =============================================================================
# RANDOM CHAT MESSAGES
# =============================================================================

RANDOM_CHAT_MESSAGES = [
    "Wave to happiness~",
    "Be happy today ⭐",
    "Jili Pudding~ 🍮",
    "✨ Twinkle Twinkle ✨",
    "Want to have pudding 🍮 together?",
    "You're doing great today! Keep it up 💪",
    "Jili loves you the most~ 🐯♥"
]

# =============================================================================
# ABOUT TEXT
# =============================================================================

ABOUT_TEXT = """Jili - Your Cute Tiger Desktop Pet

Wave to happiness, wait for bliss to come your way,
From Twinkle Twinkle ⭐"""