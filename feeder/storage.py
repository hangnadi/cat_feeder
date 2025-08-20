from __future__ import annotations
import os
import csv
from datetime import datetime
from config.settings import SETTINGS

_CSV_HEADERS = ["timestamp", "action", "grams", "result"]

def _ensure_csv_exists(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(_CSV_HEADERS)

def append_log(action: str, grams: int | None, result: str):
    path = SETTINGS.log_csv_path
    _ensure_csv_exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(timespec="seconds"), action, grams or 0, result])
