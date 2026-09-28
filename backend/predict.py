import os
import joblib
import numpy as np

class ThreatDetectionEngine:
    def __init__(self, model_path: str):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model path {model_path} does not exist. Run train.py first.")
        artifact = joblib.load(model_path)
        self.scaler = artifact["scaler"]
        self.anomaly_detector = artifact["anomaly_detector"]
        self.classifier = artifact["classifier"]

    def analyze(self, traffic_rate: float, failed_logins: float, session_duration: float, bytes_transferred: float, port_scan_count: int):
        features = np.array([[traffic_rate, failed_logins, session_duration, bytes_transferred, port_scan_count]])
        scaled = self.scaler.transform(features)

        is_anomaly = self.anomaly_detector.predict(scaled)[0] == -1
        probs = self.classifier.predict_proba(scaled)[0]
        critical_prob = float(probs[1] if len(probs) > 1 else probs[0])
        risk_score = round(critical_prob * 100, 2)

        if is_anomaly or risk_score >= 60.0:
            result = "THREAT DETECTED"
            severity = "HIGH" if risk_score >= 65.0 or failed_logins >= 20 else "MEDIUM"
        else:
            result = "NORMAL"
            severity = "SAFE"

        return {
            "result": result,
            "severity": severity,
            "is_anomaly": is_anomaly,
            "risk_score": risk_score
        }
