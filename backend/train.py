import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

print("[+] Generating high-volume enterprise network telemetry dataset...")
np.random.seed(42)
n_normal = 8000
n_attack = 1000

# Features: traffic_rate, failed_logins, session_duration, bytes_transferred, port_scan_count
normal_data = np.random.normal(loc=[25.0, 1.0, 300.0, 4500.0, 2.0], scale=[5.0, 0.5, 40.0, 500.0, 1.0], size=(n_normal, 5))
attack_data = np.random.uniform(low=[300.0, 15.0, 2.0, 25000.0, 25.0], high=[2500.0, 120.0, 30.0, 150000.0, 200.0], size=(n_attack, 5))

X = np.vstack([normal_data, attack_data])
# Target labels: 0 = Benign/Safe, 1 = Suspicious/Medium, 2 = Critical Threat (DDoS/BruteForce)
y = np.array([0] * n_normal + [2] * n_attack)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("[+] Training Dual-Model Engine: Isolation Forest + Random Forest...")
iso_forest = IsolationForest(contamination=0.11, random_state=42)
iso_forest.fit(X_scaled)

rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_scaled, y)

pipeline_artifact = {
    "scaler": scaler,
    "anomaly_detector": iso_forest,
    "classifier": rf_classifier,
    "features": ["traffic_rate", "failed_logins", "session_duration", "bytes_transferred", "port_scan_count"]
}

model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(model_dir, exist_ok=True)
joblib.dump(pipeline_artifact, os.path.join(model_dir, "threat_model.pkl"))
print("[✓] Model pipeline artifact successfully saved to models/threat_model.pkl")
