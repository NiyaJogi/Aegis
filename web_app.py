from flask import Flask, render_template, request
import os

from parser import parse_failed_attempts
from analyzer import analyze_attempts
from severity import calculate_severity, get_alert_reasons
from attack_classifier import classify_attack
from ai_copilot import analyze_security_alert


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
                "attack_type": attack_type,
                "ai_analysis": None
            })

    return alerts


@app.route("/", methods=["GET", "POST"])
def dashboard():
    filename = request.form.get("filename") or "auth.log"

    log_file = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    if request.method == "POST":

        action = request.form.get("action")

        if action == "upload":

            uploaded_file = request.files.get("log_file")

            if uploaded_file and uploaded_file.filename:

                filename = uploaded_file.filename

                log_file = os.path.join(
                    UPLOAD_FOLDER,
                    filename
                )

                uploaded_file.save(log_file)

        alerts = build_alerts(log_file)

        if action == "ai":

            selected_ip = request.form.get("alert_ip")

            for alert in alerts:

                if alert["ip"] == selected_ip:

                    alert["ai_analysis"] = analyze_security_alert(
                        ip=alert["ip"],
                        attack_type=alert["attack_type"],
                        severity=alert["severity"],
                        attempts=alert["attempts"],
                        usernames=alert["usernames"],
                        time_span=alert["time_span"],
                        reasons=alert["reasons"]
                    )

                    break

    else:
        alerts = build_alerts(log_file)

    return render_template(
        "index.html",
        alerts=alerts,
        filename=filename
    )


if __name__ == "__main__":
    app.run(debug=True)