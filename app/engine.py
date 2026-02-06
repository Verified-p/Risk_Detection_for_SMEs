import json
import joblib
import random
from app.config import MODEL_PATH, RULES_PATH

# ---- Load pre-trained Isolation Forest model ----
model = joblib.load(MODEL_PATH)

# ---- Load baseline rules ----
rules = json.load(open(RULES_PATH))


def detect(event):
    """
    Detect anomalous events using AI model and baseline rules.
    Returns:
        - score: float (negative = anomaly)
        - rule_flags: list of triggered rules (human-readable)
    """

    features = [
        event["login_hour"],
        event["device_known"],
        event["location_known"],
        event["access_count"],
        event["role_level"]
    ]

    # ---- Isolation Forest score ----
    base_score = model.decision_function([features])[0]
    score = base_score + random.uniform(-0.2, 0.2)  # demo variability

    # ---- Human-readable fields ----
    device_name = event.get("device_name", "Unknown device")
    location_name = event.get("location_name", "Unknown location")
    role_name = event.get("role_name", "Unknown role")

    rule_flags = []

    # ---- Rule 1: Login time ----
    if not rules["allowed_hours"][0] <= event["login_hour"] <= rules["allowed_hours"][1]:
        rule_flags.append("Login outside normal working hours")

    # ---- Rule 2: Unknown device ----
    if event["device_known"] == 0:
        rule_flags.append(f"Login from unknown device ({device_name})")

    # ---- Rule 3: Unknown location ----
    if event["location_known"] == 0:
        rule_flags.append(f"Login from unfamiliar location ({location_name})")

    # ---- Rule 4: High access volume ----
    if event["access_count"] > rules["max_access"]:
        rule_flags.append("Unusually high access activity")

    # ---- Rule 5: Privileged role misuse ----
    if event["role_level"] == 3 and (
        event["device_known"] == 0 or event["location_known"] == 0
    ):
        rule_flags.append(f"High-privilege role misuse detected ({role_name})")

    # ---- Occasional soft threat for realism ----
    if random.random() < 0.05:
        rule_flags.append(random.choice([
            "Suspicious rapid login attempts",
            "Unusual access pattern detected",
            "Abnormal role behavior observed"
        ]))

    return score, rule_flags

