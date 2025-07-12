import streamlit as st
import cv2
import numpy as np
from gesture_calculator import GestureCalculator
import tempfile
import os

# Add this configuration at the top
st.set_page_config(
    page_title="Hand Gesture Calculator",
    page_icon="🧮",
    layout="wide"
)

def main():
    st.title("🧮 Hand Gesture Calculator")
    st.markdown("Use hand gestures to perform calculations! Show numbers with your fingers and make gestures for operations.")
    
    # Add a warning about camera permissions
    st.warning("📷 This app requires camera access. Please allow camera permissions when prompted by your browser.")
    
    # Create columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Camera Feed")
        
        # Add camera status check
        camera_status = st.empty()
        camera_placeholder = st.empty()
        
    with col2:
        st.subheader("Calculator Display")
        display_placeholder = st.empty()
        st.subheader("Instructions")
        st.markdown("""
        **Number Gestures:**
        - 0: Closed fist
        - 1-5: Show corresponding fingers
        - 6: Thumb + pinky
        - 7: Thumb + index + middle
        - 8: Thumb + index + middle + ring
        - 9: All fingers except thumb
        
        **Operation Gestures:**
        - ➕ Addition: Peace sign (index + middle)
        - ➖ Subtraction: Thumbs down
        - ✖️ Multiplication: Cross fingers
        - ➗ Division: Point with index finger
        - 🟰 Equals: Flat palm
        - 🗑️ Clear: Wave hand
        """)
    
    # Initialize session state
    if 'calculator' not in st.session_state:
        st.session_state.calculator = GestureCalculator()
    
    # Camera controls
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        start_camera = st.button("🎥 Start Camera", type="primary", use_container_width=True)
    with col_btn2:
        stop_camera = st.button("⏹️ Stop Camera", use_container_width=True)
    
    if start_camera:
        st.session_state.camera_active = True
        camera_status.success("Camera starting...")
    if stop_camera:
        st.session_state.camera_active = False
        camera_status.info("Camera stopped")
    
    # Camera processing
    if st.session_state.get('camera_active', False):
        try:
            run_camera(camera_placeholder, display_placeholder, camera_status)
        except Exception as e:
            camera_status.error(f"Camera error: {str(e)}")
            st.session_state.camera_active = False

def run_camera(camera_placeholder, display_placeholder, camera_status):
    """Run the camera and process gestures"""
    try:
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            camera_status.error("❌ Could not open camera. Please check your camera permissions and try refreshing the page.")
            return
        
        camera_status.success("✅ Camera connected successfully!")
        calculator = st.session_state.calculator
        
        # Process a single frame (for Streamlit Cloud compatibility)
        ret, frame = cap.read()
        if ret:
            # Process frame
            processed_frame, gesture_info = calculator.process_frame(frame)
            
            # Display camera feed
            camera_placeholder.image(processed_frame, channels="BGR", use_column_width=True)
            
            # Update calculator display
            display_info = f"""
            **Current Expression:** {calculator.get_expression()}
            
            **Result:** {calculator.get_result()}
            
            **Last Gesture:** {gesture_info.get('gesture', 'None')}
            
            **Confidence:** {gesture_info.get('confidence', 0):.2f}
            """
            display_placeholder.markdown(display_info)
        else:
            camera_status.error("Failed to read from camera")
        
        cap.release()
        
    except Exception as e:
        camera_status.error(f"Camera initialization error: {str(e)}")

if __name__ == "__main__":
    main()
