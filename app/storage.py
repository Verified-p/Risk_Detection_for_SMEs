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
# SAFE EVENT SAVER (FINAL PIPELINE STEP)
# =========================================
def save_event(event, risk, reasons, blocked, rotated, verified):
    """
    Final trusted storage layer.

    Guarantees:
    ✔ No missing fields
    ✔ Reasons never None
    ✔ SQLite auto-increment works
    ✔ Works for ANY SME payload
    """

    timestamp = datetime.utcnow().isoformat()

    # ----------------------------
    # FINAL SAFETY NORMALIZATION
    # ----------------------------
    safe_event = {
        "username": event.get("username", "Unknown"),
        "ip_address": event.get("ip_address", "Unknown"),
        "session_id": event.get("session_id"),
        "device_name": event.get("device_name", "Windows Laptop"),
        "location_name": event.get("location_name", "Kisumu Office"),
        "role_name": event.get("role_name", "Unknown"),
        "action": event.get("action", "login"),
        "login_hour": event.get("login_hour"),
        "device_known": event.get("device_known"),
        "location_known": event.get("location_known"),
        "access_count": event.get("access_count"),
        "role_level": event.get("role_level"),
    }

    # ----------------------------
    # GUARANTEE REASONS
    # ----------------------------
    if not reasons:
        reasons = ["Normal login activity detected"]

    reasons_text = "; ".join(reasons)

    # ----------------------------
    # SAVE
    # ----------------------------
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