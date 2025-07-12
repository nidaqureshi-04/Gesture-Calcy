# Hand Gesture Calculator

A computer vision-powered calculator that recognizes hand gestures to perform mathematical operations.

## Features

- **Real-time gesture recognition** using MediaPipe and OpenCV
- **Number gestures** (0-9) using finger counting
- **Operation gestures** for +, -, *, /, =, and clear
- **Streamlit web interface** for easy deployment
- **Stable gesture detection** with confidence scoring

## Installation

1. Clone this repository
2. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Usage

### Local Development
\`\`\`bash
streamlit run app.py
\`\`\`

### Streamlit Cloud Deployment
1. Push your code to GitHub
2. Connect your GitHub repo to Streamlit Cloud
3. Deploy with the main file set to `app.py`

## Gesture Guide

### Numbers (0-9)
- **0**: Closed fist
- **1-5**: Show corresponding number of fingers
- **6**: Thumb + pinky extended
- **7**: Thumb + index + middle fingers
- **8**: Thumb + index + middle + ring fingers
- **9**: All fingers except thumb

### Operations
- **Addition (+)**: Peace sign (index + middle fingers)
- **Subtraction (-)**: Thumbs down
- **Division (/)**: Point with index finger
- **Equals (=)**: Flat palm
- **Clear (C)**: Wave hand

## Technical Details

### Architecture
- **Frontend**: Streamlit web interface
- **Computer Vision**: MediaPipe for hand landmark detection
- **Image Processing**: OpenCV for video capture and processing
- **Gesture Recognition**: Custom algorithm using finger counting and landmark analysis

### Key Components
1. `app.py` - Main Streamlit application
2. `gesture_calculator.py` - Core gesture recognition and calculator logic
3. `utils.py` - Utility functions for image processing
4. `config.py` - Configuration settings
5. `test_gestures.py` - Testing script for development

### Performance Optimization
- Gesture cooldown to prevent rapid-fire detection
- Gesture history for stable recognition
- Confidence scoring for reliable detection
- Optimized MediaPipe settings for real-time performance

## 🚀 Deployment Instructions

### For Streamlit Cloud (Recommended):

1. **Push to GitHub**: Upload all these files to a GitHub repository
2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repo
   - Set main file to `streamlit_app.py` (or `app.py`)
   - Click Deploy!

### Important Files for Deployment:
- `requirements.txt` - Python dependencies (updated for Streamlit Cloud)
- `packages.txt` - System packages needed for OpenCV
- `.streamlit/config.toml` - Streamlit configuration

### For Local Testing:

\`\`\`bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Or test gesture recognition directly
python test_gestures.py
\`\`\`

### Troubleshooting Deployment:

1. **If you get OpenCV errors**: The `packages.txt` file should resolve this
2. **If MediaPipe fails**: The app has fallback mode without gesture recognition
3. **Camera permissions**: Users need to allow camera access in their browser
4. **Slow loading**: First deployment may take longer due to package installation

### Browser Compatibility:
- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ⚠️ Edge (may have camera issues)

## Troubleshooting

### Common Issues
1. **Camera not working**: Check browser permissions and camera access
2. **Slow performance**: Reduce video resolution or adjust MediaPipe confidence thresholds
3. **Gesture not recognized**: Ensure good lighting and clear hand visibility
4. **Import errors**: Verify all dependencies are installed correctly

### Tips for Better Recognition
- Use good lighting conditions
- Keep hand clearly visible in frame
- Hold gestures steady for 1-2 seconds
- Maintain consistent distance from camera
- Avoid background clutter

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
