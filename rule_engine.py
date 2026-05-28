def apply_rules(text):

    text = str(text).lower()

    if "timeout" in text:
        return {
            "root_cause": "Timeout Issue",
            "comments": "Retry after service recovery",
            "severity": "High"
        }

    if "unauthorized" in text:
        return {
            "root_cause": "Authorization Failure",
            "comments": "Check user permissions",
            "severity": "Medium"
        }

    if "ora-" in text:
        return {
            "root_cause": "Database Failure",
            "comments": "Check DB connectivity",
            "severity": "Critical"
        }

    if "connection refused" in text:
        return {
            "root_cause": "Network Issue",
            "comments": "Check network services",
            "severity": "High"
        }

    return None