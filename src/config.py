import os
from os import path

from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = path.join(path.dirname(path.dirname(__file__)), "images")
CAPTURES_DIR = path.join(UPLOAD_DIR, "captures")
PREDICTIONS_DIR = path.join(UPLOAD_DIR, "predictions")

os.makedirs(CAPTURES_DIR, exist_ok=True)
os.makedirs(PREDICTIONS_DIR, exist_ok=True)

ROBOFLOW_API_URL = os.getenv("ROBOFLOW_API_URL")
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
