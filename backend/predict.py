import os
import joblib
import numpy as np
from backend.config import MODEL_PATH

class ThreatDetectionEngine:
    def __init__(self, model_path: str = MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model path {model_path} does not exist. Run train.py first.")
        artifact = joblib.load(model_path)
        self.scaler = artifact["scaler"]
        self.anomaly_detector = artifact["anomaly_detector"]
        self.classifier = artifact["classifier"]

    def analyze(self, traffic_rate: float, failed_logins: float, session_duration: float, bytes_transferred: float, port_scan_count: int):
        features = np.array([[traffic_rate, failed_logins, session_duration, bytes_transferred, port_scan_count]])
        scaled = self.scaler.transform(features)

        # Convert numpy types to standard Python primitives
        raw_anomaly = self.anomaly_detector.predict(scaled)[0]
        is_anomaly = bool(int(raw_anomaly) == -1)

        probs = self.classifier.predict_proba(scaled)[0]
        critical_prob = float(probs[-1])
        risk_score = round(float(critical_prob * 100.0), 2)

        if is_anomaly or risk_score >= 50.0:
            result = "THREAT DETECTED"
            severity = "HIGH" if (risk_score >= 60.0 or failed_logins >= 20.0 or traffic_rate > 500.0) else "MEDIUM"
        else:
            result = "NORMAL"
            severity = "SAFE"

        return {
            "result": str(result),
            "severity": str(severity),
            "is_anomaly": is_anomaly,
            "risk_score": float(risk_score)
        }

engine = ThreatDetectionEngine()
