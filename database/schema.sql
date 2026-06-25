CREATE TABLE threats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    traffic_rate REAL,
    failed_logins REAL,
    result TEXT,
    severity TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);