from flask import Flask, render_template, request
import os

from parser import parse_failed_attempts
from analyzer import analyze_attempts
from severity import calculate_severity, get_alert_reasons
from attack_classifier import classify_attack


app = Flask(__name__)

UPLOAD_FOLDER = "sample_logs"
THRESHOLD = 3

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def build_alerts(log_file):
    failed_attempts = parse_failed_attempts(log_file)

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

            attack_type = classify_attack(
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
                "reasons": reasons,
                "attack_type": attack_type
            })

    return alerts


@app.route("/", methods=["GET", "POST"])
def dashboard():

    alerts = []
    filename = None

    if request.method == "POST":

        uploaded_file = request.files.get("log_file")

        if uploaded_file and uploaded_file.filename:

            filename = uploaded_file.filename

            file_path = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            uploaded_file.save(file_path)

            alerts = build_alerts(file_path)

    else:
        default_file = "sample_logs/auth.log"

        if os.path.exists(default_file):
            alerts = build_alerts(default_file)
            filename = "auth.log"

    return render_template(
        "index.html",
        alerts=alerts,
        filename=filename
    )


if __name__ == "__main__":
    app.run(debug=True)