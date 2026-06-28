import os
from datetime import datetime

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_PATH, "Database", "logs.txt")


class Logger:
    @staticmethod
    def write_log(action: str, actor: str = "system", details: str = ""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] | ACTOR: {actor.upper()} | ACTION: {action} | DETAILS: {details}\n"
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"    Log write failed: {e}")
