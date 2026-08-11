def classify_attack(attempts, usernames, time_span):
    attempt_count = len(attempts)
    unique_user_count = len(usernames)

    if attempt_count >= 3 and time_span <= 60:
        return "SSH Brute Force"

    if unique_user_count >= 3:
        return "Username Enumeration"

    return "Suspicious SSH Activity"