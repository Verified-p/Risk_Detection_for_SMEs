def explain(score, rule_flags):
    """
    Always return meaningful, human-readable explanations.
    Dashboard must NEVER display None or empty.
    """

    reasons = []

    # rule-based explanations
    for flag in rule_flags:
        reasons.append(str(flag))

    # anomaly explanation
    if score < -0.25:
        reasons.append("Behavior deviates from normal usage pattern")

    # fallback (very important)
    if len(reasons) == 0:
        reasons.append("Normal login activity detected")

    return reasons