from mcp.server.fastmcp import FastMCP

mcp = FastMCP("exception-mcp")

# ---------------- TOOL 1 ----------------
@mcp.tool()
def get_root_cause(text: str):

    text = text.lower()

    if "timeout" in text:
        return {
            "root_cause": "Timeout Issue",
            "severity": "High"
        }

    if "ora" in text or "database" in text:
        return {
            "root_cause": "Database Failure",
            "severity": "Critical"
        }

    if "unauthorized" in text:
        return {
            "root_cause": "Auth Failure",
            "severity": "Medium"
        }

    return {
        "root_cause": "Unknown Issue",
        "severity": "Low"
    }


# ---------------- TOOL 2 ----------------
@mcp.tool()
def calculate_severity(duplicate_count: int):

    if duplicate_count > 10000:
        return "Critical"
    elif duplicate_count > 1000:
        return "High"
    elif duplicate_count > 100:
        return "Medium"
    return "Low"


# ---------------- TOOL 3 ----------------
@mcp.tool()
def detect_category(text: str):

    text = text.lower()

    if "timeout" in text:
        return ["network", "latency"]

    if "ora" in text:
        return ["database"]

    if "auth" in text:
        return ["security"]

    return ["unknown"]


if __name__ == "__main__":
    mcp.run()