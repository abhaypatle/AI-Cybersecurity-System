import os
import sys
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import DB_PATH
from backend.predict import engine
from alerts.webhook_alert import dispatch_incident_alert

app = FastAPI(
    title="AI Cybersecurity Threat Detection System",
    description="Real-Time Intrusion Detection & SIEM Engine",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

class NetworkTelemetry(BaseModel):
    source_ip: str = Field(default="127.0.0.1")
    traffic_rate: float
    failed_logins: float
    session_duration: float = 60.0
    bytes_transferred: float = 2048.0
    port_scan_count: int = 1

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS telemetry_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_ip TEXT,
            traffic_rate REAL,
            failed_logins REAL,
            risk_score REAL,
            result TEXT,
            severity TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def serve_index():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"status": "operational", "service": "AI Cybersecurity System v2.0"}

@app.post("/predict")
def predict_threat(data: NetworkTelemetry):
    try:
        verdict = engine.analyze(
            traffic_rate=data.traffic_rate,
            failed_logins=data.failed_logins,
            session_duration=data.session_duration,
            bytes_transferred=data.bytes_transferred,
            port_scan_count=data.port_scan_count
        )

        if verdict["severity"] in ["HIGH", "MEDIUM"]:
            dispatch_incident_alert(
                ip=data.source_ip,
                threat_type=verdict["result"],
                severity=verdict["severity"],
                risk_score=verdict["risk_score"]
            )

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO telemetry_audit (source_ip, traffic_rate, failed_logins, risk_score, result, severity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data.source_ip, data.traffic_rate, data.failed_logins, verdict["risk_score"], verdict["result"], verdict["severity"]))
        conn.commit()
        conn.close()

        return {
            "result": verdict["result"],
            "severity": verdict["severity"],
            "traffic_rate": data.traffic_rate,
            "failed_logins": data.failed_logins,
            "risk_score": verdict["risk_score"],
            "is_anomaly": verdict["is_anomaly"],
            "mitigation_action": "BLOCKED" if verdict["severity"] == "HIGH" else "PASS",
            "source_ip": data.source_ip
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Inference Engine Error: {str(exc)}")

@app.get("/logs")
def get_logs():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, source_ip, traffic_rate, failed_logins, risk_score, result, severity, timestamp FROM telemetry_audit ORDER BY id DESC LIMIT 50")
    rows = cur.fetchall()
    conn.close()
    return {
        "count": len(rows),
        "telemetry_stream": [
            {"id": r[0], "ip": r[1], "traffic_rate": r[2], "failed_logins": r[3], "risk_score": r[4], "result": r[5], "severity": r[6], "timestamp": r[7]}
            for r in rows
        ]
    }

# Mount static frontend assets
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
