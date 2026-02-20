from datetime import datetime

from app.engine import detect
from app.explain import explain
from app.risk import calculate
from app.storage import save_event
from app.privacy import sanitize


# =================================================
# AUTOMATED SECURITY ACTIONS
# =================================================
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


# =================================================
# 🚀 MAIN PROCESSOR
# =================================================
def process_event(event: dict):

    clean_event = sanitize(event)
    clean_event["timestamp"] = datetime.utcnow().isoformat()

    score, rule_flags = detect(clean_event)

    risk = calculate(score, len(rule_flags))

    reasons = explain(score, rule_flags)

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

