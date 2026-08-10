import re


def transform_logs(log_text):
    lines = log_text.splitlines()

    result = []
    error_count = 0
    warning_count = 0
    info_count = 0
    repeated_count = 0

    previous_message = ""

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # change date and time to HH:MM
        line = re.sub(
            r'\d{4}-\d{2}-\d{2}[ T](\d{2}):(\d{2}):\d{2}',
            r'\1:\2',
            line
        )

        # hide email
        line = re.sub(
            r'[\w.-]+@[\w.-]+\.\w+',
            '[EMAIL]',
            line
        )

        # hide IP address
        line = re.sub(
            r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            '[IP]',
            line
        )

        # make warning format same everywhere
        line = line.replace("WARNING", "WARN")

        if "ERROR" in line:
            error_count += 1
        elif "WARN" in line:
            warning_count += 1
        elif "INFO" in line:
            info_count += 1

        # get the actual message
        match = re.search(
            r'(?:INFO|WARN|ERROR)\s*[|:-]\s*(.*)',
            line
        )

        if match:
            message = match.group(1).strip()
        else:
            message = line

        if message == previous_message:
            repeated_count += 1
            result[-1] += " [REPEATED]"
        else:
            result.append(line)

        previous_message = message

    summary = [
        "",
        "----- Summary -----",
        "INFO:", str(info_count),
        "WARNINGS:", str(warning_count),
        "ERRORS:", str(error_count),
        "REPEATED:", str(repeated_count)
    ]

    return "\n".join(result + summary)


if __name__ == "__main__":
    logs = """
2026-08-09 14:32:10 | INFO | User ameysanas@gmail.com logged in
2026-08-09 14:33:01 | WARNING | Failed login from 192.168.1.42
2026-08-09 14:35:17 | ERROR | Database connection timeout
2026-08-09 14:35:18 | ERROR | Database connection timeout
"""

    print(transform_logs(logs))
