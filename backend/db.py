import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "database",
    "cybersecurity.db"
)

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS threats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    traffic_rate REAL,
    failed_logins REAL,
    result TEXT,
    severity TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ Database Created Successfully")