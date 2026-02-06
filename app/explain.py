def explain(score, rule_flags):
    reasons = list(rule_flags)

    if score < -0.25:
        reasons.append("Behavior deviates from normal usage pattern")

    return reasons
