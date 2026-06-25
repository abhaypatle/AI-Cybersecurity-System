from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import sqlite3
import os

# =============================
# FastAPI App
# =============================
app = FastAPI(
    title="AI Cybersecurity Threat Detection API",
    description="Detect cyber threats using Machine Learning",
    version="1.0"
)

# =============================
# CORS Configuration
# =============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# Load ML Model
# =============================
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "threat_model.pkl"
)

model = joblib.load(MODEL_PATH)

# =============================
# Input Schema
# =============================
class TrafficData(BaseModel):
    traffic_rate: float
    failed_logins: float

# =============================
# Home API
# =============================
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Cybersecurity Threat Detection API"
    }

# =============================
# Threat Prediction API
# =============================
@app.post("/predict")
def predict(data: TrafficData):

    X = np.array([
        [
            data.traffic_rate,
            data.failed_logins
        ]
    ])

    prediction = model.predict(X)[0]

    score = data.traffic_rate + data.failed_logins

    if prediction == -1:

        result = "THREAT DETECTED"

        if score > 400:
            severity = "HIGH"
        elif score > 100:
            severity = "MEDIUM"
        else:
            severity = "LOW"

    else:

        result = "NORMAL"
        severity = "SAFE"

    # =============================
    # Save Logs
    # =============================
    DB_PATH = os.path.join(
        os.path.dirname(__file__),
        "..",
        "database",
        "cybersecurity.db"
    )

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO threats
        (
            traffic_rate,
            failed_logins,
            result,
            severity
        )
        VALUES (?, ?, ?, ?)
    """,
    (
        data.traffic_rate,
        data.failed_logins,
        result,
        severity
    ))

    conn.commit()
    conn.close()

    return {
        "traffic_rate": data.traffic_rate,
        "failed_logins": data.failed_logins,
        "result": result,
        "severity": severity
    }

# =============================
# View Logs API
# =============================
@app.get("/logs")
def get_logs():

    DB_PATH = os.path.join(
        os.path.dirname(__file__),
        "..",
        "database",
        "cybersecurity.db"
    )

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM threats
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return {
        "total_logs": len(rows),
        "logs": rows
    }

# =============================
# Run Server
# =============================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )