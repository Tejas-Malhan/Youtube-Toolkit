import os
from datetime import datetime
LOG_FILE = os.path.join("logs", "downloads.log")
def log_download(tool_name: str, title: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {tool_name} - Downloaded: {title}\n")