import sqlite3
import json
from datetime import datetime
from app.config import DB_PATH


# =========================================
# DATABASE INIT
# =========================================
def init_db():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event TEXT,
            risk REAL,
            reasons TEXT,
            verified INTEGER DEFAULT 0,
            blocked INTEGER DEFAULT 0,
            credentials_rotated INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================================
# SAFE EVENT SAVER
# =========================================
def save_event(event, risk, reasons, blocked, rotated, verified):
    """
    Final trusted storage layer.

    Stores the REAL event exactly as received from SME systems.
    """

    timestamp = datetime.utcnow().isoformat()

    # ---------------------------------
    # KEEP REAL EVENT DATA
    # ---------------------------------
    safe_event = {
        "user": event.get("user","Unknown"),
        "ip": event.get("ip","Unknown"),
        "device": event.get("device","Unknown Device"),
        "location": event.get("location","Unknown"),
        "lat": event.get("lat"),
        "lon": event.get("lon"),
        "role": event.get("role","Unknown"),
        "login_hour": event.get("login_hour"),
        "device_known": event.get("device_known"),
        "location_known": event.get("location_known"),
        "access_count": event.get("access_count"),
    }

    # ---------------------------------
    # GUARANTEE REASONS
    # ---------------------------------
    if not reasons:
        reasons = ["Normal login activity detected"]

    reasons_text = "; ".join(reasons)

    # ---------------------------------
    # SAVE TO DATABASE
    # ---------------------------------
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        INSERT INTO audit (
            timestamp,
            event,
            risk,
            reasons,
            verified,
            blocked,
            credentials_rotated
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        json.dumps(safe_event),
        risk,
        reasons_text,
        verified,
        blocked,
        rotated
    ))

    conn.commit()
    conn.close()