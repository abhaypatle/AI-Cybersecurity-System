# AI Cybersecurity Threat Detection & SIEM Engine

An autonomous real-time Intrusion Detection System (IDS) and Security Information and Event Management (SIEM) telemetry scoring platform powered by a Dual-Model Machine Learning Engine (Isolation Forest + Random Forest).

## 🚀 Live Production Console
- **Web Dashboard:** [https://ai-cybersecurity-system-1.onrender.com/](https://ai-cybersecurity-system-1.onrender.com/)

## 🛠️ System Architecture & Tech Stack
- **Inference Engine:** FastAPI, Scikit-Learn (Unsupervised Anomaly Detection + Multi-Feature Classifier), Joblib
- **Security Telemetry:** IP Spoofing Tracking, Failed Auth Detection, Volumetric DDoS & Port Scan Identification
- **Automated Mitigation:** Policy-driven dynamic firewall blacklisting and SecOps webhook alerts
- **Containerization & Deployment:** Docker, Kubernetes Deployment Manifests, Render Cloud

## 📡 API Endpoints
- POST /predict: Ingests real-time telemetry, generates dynamic risk scores, and triggers automated defense actions.
- GET /logs: Fetches the live audit trail of flagged intrusions.
