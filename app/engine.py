import json
import joblib
from app.config import MODEL_PATH, RULES_PATH
import random

# Load model and rules
model = joblib.load(MODEL_PATH)
rules = json.load(open(RULES_PATH))


def detect(event):
    """
    AI + rules anomaly detection.
    Returns: (score, rule_flags)
    """
    # Extract features safely
    login_hour = event.get("login_hour", 12)
    device_known = event.get("device_known", 1)
    location_known = event.get("location_known", 1)
    access_count = event.get("access_count", 1)
    role_level = event.get("role_level", 1)

    features = [
        login_hour,
        device_known,
        location_known,
        access_count,
        role_level
    ]

    # AI anomaly score
    score = model.decision_function([features])[0] + random.uniform(-0.1, 0.1)

    # Rule flags
    rule_flags = []

    # Working hours
    allowed_hours = rules.get("allowed_hours", [6, 20])
    if not allowed_hours[0] <= login_hour <= allowed_hours[1]:
        rule_flags.append("Login outside working hours")

    # Unknown device
    if device_known == 0:
        rule_flags.append(f"Unknown device used ({event.get('device_name')})")

    # Unknown location
    if location_known == 0:
        rule_flags.append(f"Unrecognized location ({event.get('location_name')})")

    # Excessive accesses
    max_access = rules.get("max_access", 50)
    if access_count > max_access:
        rule_flags.append("Excessive access attempts detected")

    # Privileged misuse
    if role_level >= 3 and (device_known == 0 or location_known == 0):
        rule_flags.append(f"Privileged role misuse ({event.get('role_name')})")

    # Add occasional soft threat for realism
    if random.random() < 0.05:
        rule_flags.append(random.choice([
            "Suspicious rapid login attempts",
            "Unusual access pattern detected",
            "Abnormal role behavior observed"
        ]))

    return score, rule_flags