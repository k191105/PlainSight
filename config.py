import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///plainsight.db')  # Default to SQLite for development

# If we're in production (Streamlit Cloud), use PostgreSQL
if os.getenv('STREAMLIT_SERVER_RUNNING', 'false').lower() == 'true':
    DATABASE_URL = os.getenv('DATABASE_URL')  # This will be set in Streamlit Cloud

# Application configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')  # Change this in production
DEFAULT_CREDITS = 5  # Number of credits new users get

# OpenAI configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Session configuration
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = False 