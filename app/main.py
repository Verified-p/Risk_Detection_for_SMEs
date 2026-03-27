from datetime import datetime
import sqlite3
from app.privacy import sanitize
from app.engine import detect
from app.risk import calculate
from app.explain import explain
from app.storage import save_event

# =========================
# DATABASE
# =========================
DB = "trustlensai.db"

def is_valid_user(username: str) -> bool:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY)")  # ensure table exists
    cur.execute("SELECT 1 FROM users WHERE username=?", (username,))
    result = cur.fetchone()
    conn.close()
    return result is not None

# =========================
# ACTIONS
# =========================
def execute_actions(risk: float):
    verified = 0
    blocked = 0
    rotated = 0
    if risk >= 70:
        blocked = 1
        rotated = 1
    elif risk >= 40:
        blocked = 1
    else:
        verified = 1
    return verified, blocked, rotated

# =========================
# MAIN PROCESSOR
# =========================
def process_event(event: dict):
    # sanitize input
    clean_event = sanitize(event)
    clean_event["timestamp"] = datetime.utcnow().isoformat()

    # Get real fields from incoming event
    username = event.get("user", "Unknown")
    ip = event.get("ip", "Unknown")
    device = event.get("device", "Unknown Device")
    location = event.get("location", "Unknown Location")
    unknown_user_flag = event.get("unknown_user", 0)

    # Determine role
    if unknown_user_flag or not is_valid_user(username):
        role = "unknown"
    else:
        role = "user"

    # store the real values
    clean_event["user"] = username
    clean_event["ip"] = ip
    clean_event["device"] = device
    clean_event["location"] = location
    clean_event["role"] = role

    # Detect AI risk
    score, rule_flags = detect(clean_event)

    # increase risk if unknown user
    if role == "unknown":
        score += 70
        rule_flags.append("Unknown user / not registered by admin")

    risk = calculate(score, len(rule_flags))
    reasons = explain(score, rule_flags)
    verified, blocked, rotated = execute_actions(risk)

    # Save to database
    save_event(clean_event, risk, reasons, blocked, rotated, verified)

    return {
        "risk": int(risk),
        "verified": verified,
        "blocked": blocked,
        "credentials_rotated": rotated,
        "reasons": reasons
    }