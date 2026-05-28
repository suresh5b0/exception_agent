import asyncio
from agent import analyze_exception
from rule_engine import apply_rules
from log_parser import parse_log

MAX_CONCURRENT = 10
semaphore = asyncio.Semaphore(MAX_CONCURRENT)

async def process_group(row):

    async with semaphore:

        text = row["exception_details"]
        dup = row["duplicate_count"]

        rule = apply_rules(text)
        if rule:
            return {
                "normalized": row["normalized"],
                **rule
            }

        categories = parse_log(text)

        result = await analyze_exception(text, dup, categories)

        return {
            "normalized": row["normalized"],
            **result
        }

async def process_all(df):

    tasks = [process_group(row) for _, row in df.iterrows()]
    return await asyncio.gather(*tasks)