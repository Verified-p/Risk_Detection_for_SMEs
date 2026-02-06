from app.engine import detect
from app.explain import explain
from app.risk import calculate
from app.storage import log
from app.privacy import sanitize


def process_event(event: dict) -> dict:
    """
    Central processing pipeline for TrustLens AI
    """

    # 1️⃣ Sanitize input (privacy-first)
    clean_event = sanitize(event)

    # 2️⃣ Detect anomalies (AI + rules)
    score, rule_flags = detect(clean_event)

    # 3️⃣ Calculate final risk percentage
    risk = calculate(score, len(rule_flags))

    # 4️⃣ Generate human-readable explanations
    reasons = explain(score, rule_flags)

    # 5️⃣ Persist audit log (NO sensitive data)
    log(clean_event, risk, reasons)

    # 6️⃣ Return result to UI / API
    return {
        "risk": int(risk),
        "reasons": reasons
    }
