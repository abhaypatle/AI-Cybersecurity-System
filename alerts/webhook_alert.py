import logging
import requests
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SecOpsNotifier")

def dispatch_incident_alert(ip: str, threat_type: str, severity: str, risk_score: float):
    alert_payload = {
        "event": "CYBER_THREAT_DETECTED",
        "source_ip": ip,
        "classification": threat_type,
        "severity": severity,
        "risk_score": f"{risk_score}%",
        "action_taken": "IP_BLACKLISTED_AUTOMATED_DEFENSE"
    }
    logger.critical(f"[ACTIVE DEFENSE TRIGGERED] {json.dumps(alert_payload)}")
    
    # Optional webhook URL for Discord / Slack / AWS Lambda
    webhook_url = os.getenv("INCIDENT_WEBHOOK_URL")
    if webhook_url:
        try:
            requests.post(webhook_url, json=alert_payload, timeout=3)
        except Exception as e:
            logger.error(f"Failed to transmit alert to webhook: {e}")
    return alert_payload
