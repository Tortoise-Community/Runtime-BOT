import gzip
import json
import time
from decouple import config

NEW_RELIC_LOG_URL = "https://log-api.eu.newrelic.com/log/v1"
NEW_RELIC_LICENSE_KEY = config("NEW_RELIC_LICENSE_KEY")


async def log_user_code(session, user_id: int, code: str):
    if len(code) > 4000:
        code = code[:4000] + "...(truncated)"

    payload = [{
        "message": "user_code_submission",
        "user_id": user_id,
        "code": code,
        "timestamp": int(time.time() * 1000),  # ms
    }]

    data = json.dumps(payload).encode("utf-8")

    if len(data) > 1_000_000:
        return

    compressed = gzip.compress(data)

    headers = {
        "Content-Type": "application/json",
        "Content-Encoding": "gzip",
        "Api-Key": NEW_RELIC_LICENSE_KEY,
    }

    try:
        await session.post(
            NEW_RELIC_LOG_URL,
            data=compressed,
            headers=headers,
        )
    except Exception:
        pass