def calculate(score, rule_count):
    """
    Convert anomaly score + rule triggers into 0–100 risk.
    Ensures:
    - High risk ≥ 70 for suspicious events
    - Medium risk 41–69 for partially suspicious
    - Low risk 0–40 for normal events
    """
    # AI contribution: negative = anomaly
    ai_risk = max(0, (-score) * 60)  # higher weight than before

    # Rule contribution
    rule_risk = rule_count * 20  # each triggered rule adds 20%

    # Combine
    total_risk = ai_risk + rule_risk

    # Enforce risk bands
    if rule_count >= 3 or ai_risk > 50:
        total_risk = max(total_risk, 70)  # HIGH risk
    elif rule_count == 2 or (ai_risk > 20 and ai_risk <= 50):
        total_risk = max(min(total_risk, 69), 41)  # MEDIUM risk
    else:
        total_risk = min(total_risk, 40)  # LOW risk

    return min(100, int(total_risk))