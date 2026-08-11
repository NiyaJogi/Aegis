import sys

from parser import parse_failed_attempts
from analyzer import analyze_attempts
from severity import calculate_severity
from report import write_alert


REPORT_FILE = "reports/suspicious_report.txt"
THRESHOLD = 3


if len(sys.argv) < 2:
    print("Usage: python3 app.py <log_file>")
    sys.exit(1)


LOG_FILE = sys.argv[1]


failed_attempts = parse_failed_attempts(LOG_FILE)


with open(REPORT_FILE, "w") as report:

    for ip, attempts in failed_attempts.items():

        if len(attempts) >= THRESHOLD:

            usernames, time_span = analyze_attempts(attempts)

            severity = calculate_severity(
                attempts,
                usernames,
                time_span
            )

            write_alert(
                report,
                ip,
                attempts,
                usernames,
                time_span,
                severity
            )


print(
    f"Analysis complete. "
    f"Report saved to {REPORT_FILE}"
)