import json
import ollama
from prompts import SYSTEM_PROMPT
import os

MODEL = "llama3.2"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

async def analyze_exception(text, duplicate_count, categories):

    payload = {
        "exception": text,
        "duplicate_count": duplicate_count,
        "categories": categories
    }

    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(payload)}
        ],
        format="json"
    )

    try:
        result = json.loads(response["message"]["content"])

        return {
            "root_cause": result.get("root_cause", "Unknown"),
            "comments": result.get("comments", "Needs review"),
            "severity": result.get("severity", "Medium")
        }

    except:
        return {
            "root_cause": "Parsing Error",
            "comments": "Invalid AI response",
            "severity": "Medium"
        }