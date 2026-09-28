import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "threat_model.pkl")
DB_PATH = os.path.join(BASE_DIR, "database", "cybersecurity.db")
