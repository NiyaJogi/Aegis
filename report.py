def write_alert(
    report,
    ip,
    attempts,
    usernames,
    time_span,
    severity
):
    report.write("=" * 60 + "\n")
    report.write("SECURITY ALERT\n")
    report.write("=" * 60 + "\n")

    report.write(f"Source IP: {ip}\n")
    report.write(f"Failed Attempts: {len(attempts)}\n")

    report.write(
        f"Targeted Accounts: {', '.join(usernames)}\n"
    )

    report.write(
        f"Time Span: {time_span:.0f} seconds\n"
    )

    report.write(f"Severity: {severity}\n")

    report.write("\nSummary:\n")

    report.write(
        f"{ip} generated {len(attempts)} "
        f"failed SSH login attempts targeting "
        f"{', '.join(usernames)} "
        f"within {time_span:.0f} seconds.\n"
    )

    report.write("\nEvidence:\n")

    for attempt in attempts:
        report.write(f"    {attempt}\n")

    report.write("\n")