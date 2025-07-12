"""Configuration settings for the gesture calculator app"""

# Camera settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Gesture recognition settings
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5
GESTURE_COOLDOWN = 1.0  # seconds between gesture recognitions
GESTURE_HISTORY_SIZE = 5  # number of frames to consider for stable gesture

# UI settings
STREAMLIT_THEME = {
    "primaryColor": "#FF6B6B",
    "backgroundColor": "#FFFFFF",
    "secondaryBackgroundColor": "#F0F2F6",
    "textColor": "#262730"
}
