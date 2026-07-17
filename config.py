"""
config.py

Application configuration.
"""

from pathlib import Path
import os


# -------------------------------------------------
# Project Paths
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

CREDENTIALS_FILE = DATA_DIR / "credentials.json"


# -------------------------------------------------
# Google Sheets
# -------------------------------------------------

SPREADSHEET_NAME = "Compass"
SPREADSHEET_ID = "1ElMohLKNO1bpKNeypGYCGcD-LOtVlHmRvc96BC-0pq8"


# -------------------------------------------------
# Currency
# -------------------------------------------------

DEFAULT_CURRENCY = "INR"


# -------------------------------------------------
# Date Format
# -------------------------------------------------

DATE_FORMAT = "%Y-%m-%d"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


# -------------------------------------------------
# Logging
# -------------------------------------------------

LOG_LEVEL = "INFO"


# -------------------------------------------------
# Application
# -------------------------------------------------

APP_NAME = "Compass"

APP_VERSION = "1.0.0"

DEBUG = os.getenv("DEBUG", "False").lower() == "true"