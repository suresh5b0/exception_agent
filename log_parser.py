import re

def parse_log(text):

    patterns = {
        "timeout": r"timeout|timed out",
        "database": r"ORA-|SQL",
        "api": r"500|502|503",
        "auth": r"unauthorized|forbidden",
        "network": r"connection refused|host unreachable"
    }

    detected = []

    text = str(text).lower()

    for k, v in patterns.items():
        if re.search(v, text):
            detected.append(k)

    return detected