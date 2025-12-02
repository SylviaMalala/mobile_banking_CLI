"""
Configuration settings for the mobile banking CLI application.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+pysqlite:///./bank.db")

# Application settings
APP_NAME = os.getenv("APP_NAME", "CLI Bank")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Security settings (for future implementation)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
PASSWORD_SALT = os.getenv("PASSWORD_SALT", "dev-salt-change-in-production")

# Database settings
DB_ECHO = DEBUG  # Echo SQL queries in debug mode
