from collections import defaultdict


def parse_failed_attempts(log_file):
    failed_attempts = defaultdict(list)

    with open(log_file, "r") as file:

        for line in file:

            if "Failed password" in line and "from" in line:

                parts = line.split()

                try:

                    ip_index = parts.index("from") + 1
                    ip_address = parts[ip_index]

                    failed_attempts[ip_address].append(
                        line.strip()
                    )

                except (ValueError, IndexError):
                    continue

    return failed_attempts