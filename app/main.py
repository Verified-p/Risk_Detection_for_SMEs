from datetime import datetime
from app.storage import save_event
from app.privacy import sanitize


# =========================================
# Security actions
# =========================================
def execute_actions(risk: float):
    verified = 0
    blocked = 0
    rotated = 0

    if risk >= 70:
        blocked = 1
        rotated = 1
    else:
        verified = 1

    return verified, blocked, rotated


# =========================================
# MAIN PROCESSOR (NO DATABASE CHECKS)
# =========================================
def process_event(event: dict):

    clean_event = sanitize(event)
    clean_event["timestamp"] = datetime.utcnow().isoformat()

    unknown = event.get("unknown_user", 1)

    # ⭐ ONLY use Bank flag
    if unknown == 1:
        risk = 90
        reasons = ["Unknown user / not registered by admin"]
        clean_event["role"] = "Unknown"
    else:
        risk = 10
        reasons = ["Normal login activity detected"]

    verified, blocked, rotated = execute_actions(risk)

    save_event(
        clean_event,
        risk,
        reasons,
        blocked,
        rotated,
        verified
    )

    return {
        "risk": int(risk),
        "verified": verified,
        "blocked": blocked,
        "credentials_rotated": rotated,
        "reasons": reasons
    }