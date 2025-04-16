import os
import streamlit as st
from dotenv import load_dotenv

# First try to load from Streamlit secrets (for Streamlit Cloud)
try:
    DATABASE_URL = st.secrets["DATABASE_URL"]
    SECRET_KEY = st.secrets["SECRET_KEY"]
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except Exception:
    # If that fails (local development), load from .env file
    load_dotenv()
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///plainsight.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Application configuration
DEFAULT_CREDITS = 5  # Number of credits new users get

# Session configuration
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = False