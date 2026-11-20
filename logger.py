import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

LOG_FILE = "bot_log.json"
IST = ZoneInfo("Asia/Kolkata")


def log_this(userID: int | None, chatID: int | None, content: str | None) -> None:

    entry = {
        "timestamp" : datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S %Z"),
        "user_id" : userID,
        "chat_id" : chatID,
        "content" : content or "[Not a text]"
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write( json.dumps(entry, ensure_ascii=False) + "\n")
