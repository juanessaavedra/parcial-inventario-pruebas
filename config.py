# config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    # Claves secretas desde variables de entorno
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-fallback'
    
    # Base de datos desde variable de entorno
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql+psycopg://juanessaavedra@localhost:5432/inventario'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    
    # BD y Redis de testing desde variables de entorno
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'postgresql+psycopg://postgres:admin@localhost:5432/inventario_test'