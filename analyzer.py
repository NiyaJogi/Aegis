from datetime import datetime


def get_username(log_line):
    parts = log_line.split()

    try:
        if "invalid user" in log_line:
            user_index = parts.index("user") + 1

        elif "for user" in log_line:
            user_index = parts.index("user") + 1

        else:
            user_index = parts.index("for") + 1

        return parts[user_index]

    except (ValueError, IndexError):
        return "unknown"


def get_timestamp(log_line):
    parts = log_line.split()

    timestamp_text = " ".join(parts[0:3])

    return datetime.strptime(
        timestamp_text,
        "%b %d %H:%M:%S"
    )


def analyze_attempts(attempts):
    usernames = []

    for attempt in attempts:
        username = get_username(attempt)
        usernames.append(username)

    unique_usernames = sorted(set(usernames))

    timestamps = [
        get_timestamp(attempt)
        for attempt in attempts
    ]

    first_attempt = min(timestamps)
    last_attempt = max(timestamps)

    time_span = (
        last_attempt - first_attempt
    ).total_seconds()

    return unique_usernames, time_span