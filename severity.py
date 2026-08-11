def calculate_severity(attempts, usernames, time_span):
    attempt_count = len(attempts)

    if attempt_count >= 3 and time_span <= 60:
        return "HIGH"

    if "root" in usernames or attempt_count >= 10:
        return "HIGH"

    elif attempt_count >= 5:
        return "MEDIUM"

    else:
        return "LOW"


def get_alert_reasons(attempts, usernames, time_span):
    reasons = []

    if len(attempts) >= 3:
        reasons.append(
            f"{len(attempts)} failed login attempts detected"
        )

    if "root" in usernames:
        reasons.append(
            "Privileged account 'root' was targeted"
        )

    if time_span <= 60:
        reasons.append(
            f"Authentication attempts occurred within {time_span:.0f} seconds"
        )

    if len(usernames) > 1:
        reasons.append(
            f"Multiple accounts were targeted: {', '.join(usernames)}"
        )

    return reasons