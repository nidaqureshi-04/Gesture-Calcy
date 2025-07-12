# Alternative main file for Streamlit Cloud
import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

# Import and run the main app
from app import main

if __name__ == "__main__":
    main()
