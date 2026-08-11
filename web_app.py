from flask import Flask, render_template
from parser import parse_failed_attempts
from analyzer import analyze_attempts
from severity import calculate_severity, get_alert_reasons

app = Flask(__name__)

LOG_FILE = "sample_logs/auth.log"
THRESHOLD = 3


@app.route("/")
def dashboard():
    failed_attempts = parse_failed_attempts(LOG_FILE)

    alerts = []

    for ip, attempts in failed_attempts.items():
        if len(attempts) >= THRESHOLD:

            usernames, time_span = analyze_attempts(attempts)

            severity = calculate_severity(
                attempts,
                usernames,
                time_span
            )

            reasons = get_alert_reasons(
                attempts,
                usernames,
                time_span
            )

            alerts.append({
                "ip": ip,
                "attempts": len(attempts),
                "usernames": usernames,
                "time_span": time_span,
                "severity": severity,
                "reasons": reasons
            })

    return render_template(
        "index.html",
        alerts=alerts
    )


if __name__ == "__main__":
    app.run(debug=True)