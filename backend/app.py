import os
import sys
import sqlite3
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import DB_PATH, MODEL_PATH
from backend.predict import ThreatDetectionEngine
from alerts.webhook_alert import dispatch_incident_alert

app = FastAPI(
    title="AI Cybersecurity Threat Detection System",
    description="Real-time Network Threat Scoring, SIEM Ingestion, and Automated Incident Defense API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = ThreatDetectionEngine(MODEL_PATH)

class NetworkTelemetry(BaseModel):
    source_ip: str = Field(default="192.168.1.100", description="Origin IPv4 address")
    traffic_rate: float = Field(..., ge=0.0, description="Packets/Requests per second")
    failed_logins: float = Field(..., ge=0.0, description="Failed authentication attempts")
    session_duration: float = Field(default=60.0, ge=0.0, description="Session longevity in seconds")
    bytes_transferred: float = Field(default=2048.0, ge=0.0, description="Volume of payload transferred")
    port_scan_count: int = Field(default=1, ge=0, description="Targeted unique ports")

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

@app.get("/", tags=["Health"])
def health_status():
    return {"system": "Active Defense Engine", "status": "operational", "version": "2.0.0"}

@app.post("/predict", tags=["Inference"])
def evaluate_traffic(data: NetworkTelemetry):
    try:
        verdict = engine.analyze(
            data.traffic_rate,
            data.failed_logins,
            data.session_duration,
            data.bytes_transferred,
            data.port_scan_count
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
            "source_ip": data.source_ip,
            "analysis": verdict,
            "mitigation_action": "BLOCKED" if verdict["severity"] == "HIGH" else "PASS"
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/logs", tags=["Audit"])
def fetch_telemetry_logs():
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
