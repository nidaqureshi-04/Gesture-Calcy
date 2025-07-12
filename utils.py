"""Utility functions for the gesture calculator"""

import cv2
import numpy as np
from typing import List, Tuple

def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two points"""
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calculate_angle(point1: Tuple[float, float], point2: Tuple[float, float], point3: Tuple[float, float]) -> float:
    """Calculate angle between three points"""
    vector1 = np.array([point1[0] - point2[0], point1[1] - point2[1]])
    vector2 = np.array([point3[0] - point2[0], point3[1] - point2[1]])
    
    cos_angle = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
    return np.degrees(angle)

def smooth_landmarks(landmarks_history: List, window_size: int = 5) -> List:
    """Smooth landmark positions using moving average"""
    if len(landmarks_history) < window_size:
        return landmarks_history[-1] if landmarks_history else []
    
    # Take the last window_size frames
    recent_landmarks = landmarks_history[-window_size:]
    
    # Calculate average for each landmark
    smoothed = []
    for i in range(len(recent_landmarks[0])):
        avg_x = sum(frame[i].x for frame in recent_landmarks) / window_size
        avg_y = sum(frame[i].y for frame in recent_landmarks) / window_size
        avg_z = sum(frame[i].z for frame in recent_landmarks) / window_size
        
        # Create a simple object with x, y, z attributes
        class Landmark:
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z
        
        smoothed.append(Landmark(avg_x, avg_y, avg_z))
    
    return smoothed

def draw_gesture_guide(frame: np.ndarray) -> np.ndarray:
    """Draw gesture guide on the frame"""
    height, width = frame.shape[:2]
    
    # Create semi-transparent overlay
    overlay = frame.copy()
    
    # Draw guide box
    cv2.rectangle(overlay, (width - 300, 10), (width - 10, 200), (0, 0, 0), -1)
    
    # Add guide text
    guide_text = [
        "Gesture Guide:",
        "0-5: Show fingers",
        "6: Thumb + Pinky",
        "+: Peace sign",
        "-: Thumbs down",
        "/: Point finger",
        "=: Flat palm",
        "C: Wave hand"
    ]
    
    for i, text in enumerate(guide_text):
        y_pos = 30 + i * 20
        cv2.putText(overlay, text, (width - 290, y_pos), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    # Blend overlay with original frame
    alpha = 0.7
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    
    return frame
