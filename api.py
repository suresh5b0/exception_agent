from fastapi import FastAPI
import json
import ollama
from mcp import ClientSession

app = FastAPI(title="Exception Analyzer API")

MODEL = "llama3.2"
MCP_SERVER_URL = "http://localhost:8000"


# ---------------- CORE RCA ENGINE ----------------
async def run_rca(exception_text: str, duplicate_count: int):

    async with ClientSession(MCP_SERVER_URL) as session:

        # -------- MCP TOOL CALLS --------
        rc = await session.call_tool(
            "get_root_cause",
            {"text": exception_text}
        )

        severity = await session.call_tool(
            "calculate_severity",
            {"duplicate_count": duplicate_count}
        )

        category = await session.call_tool(
            "detect_category",
            {"text": exception_text}
        )

    # -------- BUILD CONTEXT --------
    payload = {
        "exception": exception_text,
        "duplicate_count": duplicate_count,
        "tool_root_cause": rc,
        "tool_severity": severity,
        "category": category
    }

    # -------- OLLAMA CALL --------
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a production RCA engine. Return strict JSON."
            },
            {
                "role": "user",
                "content": json.dumps(payload)
            }
        ],
        format="json"
    )

    return json.loads(response["message"]["content"])


# ---------------- API ENDPOINT ----------------
@app.post("/analyze")
async def analyze(data: dict):

    result = await run_rca(
        data["exception"],
        data["duplicate_count"]
    )

    return result