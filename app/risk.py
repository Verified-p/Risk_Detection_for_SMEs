def calculate(score, rule_count):
    """
    Calculate combined risk score from AI anomaly score and rule triggers.

    score: Isolation Forest score (negative = anomaly)
    rule_count: number of triggered rules

    Returns: risk percentage (0-100)
    """

    # ---- AI contribution ----
    # Negative scores indicate anomaly → convert to positive risk
    ai_risk = max(0, (-score) * 60)  # Slightly lower weight than before for smoother scaling

    # ---- Rule contribution ----
    rule_risk = rule_count * 20  # Each triggered rule adds 20%

    # ---- Combined raw risk ----
    total_risk = ai_risk + rule_risk

    # ---- Enforce risk bands ----
    if rule_count >= 3 or ai_risk > 50:
        # High-risk scenario → force minimum 70%
        total_risk = max(total_risk, 70)
    elif rule_count == 2 or (ai_risk > 20 and ai_risk <= 50):
        # Medium-risk scenario → clamp to 41-69%
        total_risk = max(min(total_risk, 69), 41)
    else:
        # Low-risk → clamp to 0-40%
        total_risk = min(total_risk, 40)

    return min(100, int(total_risk))
