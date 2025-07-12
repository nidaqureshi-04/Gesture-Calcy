"""Test script to verify gesture recognition functionality"""

import cv2
import numpy as np
from gesture_calculator import GestureCalculator

def test_gesture_recognition():
    """Test the gesture recognition system"""
    calculator = GestureCalculator()
    cap = cv2.VideoCapture(0)
    
    print("Testing Gesture Recognition System")
    print("Press 'q' to quit, 'r' to reset calculator")
    print("Show different hand gestures to test recognition")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process frame
        processed_frame, gesture_info = calculator.process_frame(frame)
        
        # Display information
        cv2.putText(processed_frame, f"Expression: {calculator.get_expression()}", 
                   (10, processed_frame.shape[0] - 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(processed_frame, f"Result: {calculator.get_result()}", 
                   (10, processed_frame.shape[0] - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(processed_frame, f"Last Gesture: {gesture_info.get('gesture', 'None')}", 
                   (10, processed_frame.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        cv2.imshow('Gesture Calculator Test', processed_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            calculator.clear()
            print("Calculator reset")
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_gesture_recognition()
