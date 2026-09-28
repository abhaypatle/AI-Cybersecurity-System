import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SecurityAlerts")

def send_security_alert(ip: str, traffic_rate: float, failed_logins: float, severity: str):
    message = f"[CRITICAL THREAT ALERT] Source IP: {ip} | Traffic: {traffic_rate} req/s | Failed Logins: {failed_logins} | Severity: {severity}"
    logger.warning(message)
    # Production note: AWS SNS ya SMTP integration yahan connect hota hai
    return {"status": "dispatched", "target": "SecOps Team", "alert": message}
