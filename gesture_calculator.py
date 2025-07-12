import cv2
import numpy as np
import time
from typing import Dict, Tuple, Optional

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("MediaPipe not available, using fallback mode")

class GestureCalculator:
    def __init__(self):
        # Initialize MediaPipe if available
        if MEDIAPIPE_AVAILABLE:
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )
            self.mp_draw = mp.solutions.drawing_utils
        else:
            self.mp_hands = None
            self.hands = None
            self.mp_draw = None
        
        # Calculator state
        self.expression = ""
        self.result = "0"
        self.last_gesture = None
        self.last_gesture_time = 0
        self.gesture_cooldown = 1.0  # seconds
        
        # Gesture history for stability
        self.gesture_history = []
        self.history_size = 5
    
    def count_fingers(self, landmarks) -> int:
        """Count the number of extended fingers"""
        if not landmarks:
            return 0
            
        # Finger tip and pip landmarks
        tip_ids = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky
        pip_ids = [3, 6, 10, 14, 18]  # corresponding pip joints
        
        fingers = []
        
        # Thumb (different logic due to orientation)
        if landmarks[tip_ids[0]].x > landmarks[pip_ids[0]].x:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Other fingers
        for i in range(1, 5):
            if landmarks[tip_ids[i]].y < landmarks[pip_ids[i]].y:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return sum(fingers)
    
    def detect_gesture(self, landmarks) -> Dict:
        """Detect specific gestures from hand landmarks"""
        if not landmarks:
            return {"gesture": "unknown", "confidence": 0.0}
            
        finger_count = self.count_fingers(landmarks)
        
        # Get landmark positions
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        gesture_info = {"gesture": "unknown", "confidence": 0.0}
        
        # Number gestures (0-9)
        if finger_count == 0:
            gesture_info = {"gesture": "0", "confidence": 0.9}
        elif finger_count == 1:
            gesture_info = {"gesture": "1", "confidence": 0.9}
        elif finger_count == 2:
            # Check if it's peace sign (addition) or just 2
            if (landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y and 
                landmarks[16].y > landmarks[14].y and landmarks[20].y > landmarks[18].y):
                gesture_info = {"gesture": "+", "confidence": 0.8}
            else:
                gesture_info = {"gesture": "2", "confidence": 0.9}
        elif finger_count == 3:
            gesture_info = {"gesture": "3", "confidence": 0.9}
        elif finger_count == 4:
            gesture_info = {"gesture": "4", "confidence": 0.9}
        elif finger_count == 5:
            # Check if it's a flat palm (equals) or just 5
            palm_flatness = self.check_palm_flatness(landmarks)
            if palm_flatness > 0.7:
                gesture_info = {"gesture": "=", "confidence": 0.8}
            else:
                gesture_info = {"gesture": "5", "confidence": 0.9}
        
        # Special number gestures
        elif finger_count == 2 and landmarks[4].y < landmarks[3].y and landmarks[20].y < landmarks[19].y:
            gesture_info = {"gesture": "6", "confidence": 0.8}  # Thumb + pinky
        
        # Operation gestures
        if landmarks[4].y > landmarks[3].y and finger_count == 1:  # Thumbs down
            gesture_info = {"gesture": "-", "confidence": 0.8}
        
        # Point gesture (division)
        if (finger_count == 1 and landmarks[8].y < landmarks[6].y and 
            landmarks[12].y > landmarks[10].y):
            gesture_info = {"gesture": "/", "confidence": 0.8}
        
        # Wave gesture (clear)
        if finger_count >= 4 and abs(landmarks[8].x - landmarks[12].x) > 0.1:
            gesture_info = {"gesture": "C", "confidence": 0.7}
        
        return gesture_info
    
    def check_palm_flatness(self, landmarks) -> float:
        """Check how flat the palm is (for equals gesture)"""
        if not landmarks or len(landmarks) < 21:
            return 0.0
            
        # Calculate the variance in y-coordinates of fingertips
        fingertips = [landmarks[8], landmarks[12], landmarks[16], landmarks[20]]
        y_coords = [tip.y for tip in fingertips]
        variance = np.var(y_coords)
        
        # Lower variance means flatter palm
        flatness = max(0, 1 - variance * 10)
        return flatness
    
    def process_gesture(self, gesture_info: Dict):
        """Process the detected gesture and update calculator state"""
        current_time = time.time()
        gesture = gesture_info.get("gesture", "")
        confidence = gesture_info.get("confidence", 0)
        
        # Add to history for stability
        self.gesture_history.append(gesture)
        if len(self.gesture_history) > self.history_size:
            self.gesture_history.pop(0)
        
        # Check if gesture is stable (appears multiple times)
        if self.gesture_history.count(gesture) < 3:
            return
        
        # Check cooldown
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return
        
        # Ignore if same as last gesture
        if gesture == self.last_gesture:
            return
        
        # Process the gesture
        if gesture.isdigit():
            self.add_number(gesture)
        elif gesture in ["+", "-", "*", "/"]:
            self.add_operator(gesture)
        elif gesture == "=":
            self.calculate()
        elif gesture == "C":
            self.clear()
        
        self.last_gesture = gesture
        self.last_gesture_time = current_time
    
    def add_number(self, number: str):
        """Add a number to the expression"""
        if self.result != "0" and self.expression == "":
            self.expression = number
        else:
            self.expression += number
        self.update_display()
    
    def add_operator(self, operator: str):
        """Add an operator to the expression"""
        if self.expression and not self.expression[-1] in "+-*/":
            self.expression += operator
        self.update_display()
    
    def calculate(self):
        """Calculate the result of the expression"""
        try:
            if self.expression:
                # Replace * with * for multiplication (if using x)
                expr = self.expression.replace("x", "*")
                self.result = str(eval(expr))
                self.expression = ""
        except:
            self.result = "Error"
            self.expression = ""
        self.update_display()
    
    def clear(self):
        """Clear the calculator"""
        self.expression = ""
        self.result = "0"
        self.update_display()
    
    def update_display(self):
        """Update the display (placeholder for now)"""
        pass
    
    def get_expression(self) -> str:
        """Get current expression"""
        return self.expression if self.expression else "0"
    
    def get_result(self) -> str:
        """Get current result"""
        return self.result
    
    def process_frame(self, frame) -> Tuple[np.ndarray, Dict]:
        """Process a video frame and return annotated frame with gesture info"""
        if frame is None:
            return np.zeros((480, 640, 3), dtype=np.uint8), {"gesture": "None", "confidence": 0.0}
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        gesture_info = {"gesture": "None", "confidence": 0.0}
        
        if MEDIAPIPE_AVAILABLE and self.hands is not None:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Detect gesture
                    gesture_info = self.detect_gesture(hand_landmarks.landmark)
                    self.process_gesture(gesture_info)
                    
                    # Draw gesture text
                    cv2.putText(frame, f"Gesture: {gesture_info['gesture']}", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f"Confidence: {gesture_info['confidence']:.2f}", 
                               (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            # Fallback mode without MediaPipe
            cv2.putText(frame, "MediaPipe not available", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, "Manual input mode", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Draw calculator display on frame
        cv2.putText(frame, f"Expression: {self.get_expression()}", 
                   (10, frame.shape[0] - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, f"Result: {self.get_result()}", 
                   (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        return frame, gesture_info
