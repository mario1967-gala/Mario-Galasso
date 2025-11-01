import os
from dotenv import load_dotenv

# Carica variabili d'ambiente dal file .env
load_dotenv()

class Config:
    """Configurazione dell'applicazione"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'didattica.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size

    # API Keys
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
