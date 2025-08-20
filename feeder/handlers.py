from __future__ import annotations
import json
from datetime import datetime
from typing import Callable
from feeder.device import DeviceState
from feeder.storage import append_log

# Message format examples:
# "FEED 50"
# "STATUS?"
# (You could switch to JSON later for richer commands.)

def handle_message(payload: str, device: DeviceState, publish_event: Callable[[str], None]) -> None:
    msg = payload.strip()
    if not msg:
        return

    if msg.upper().startswith("FEED"):
        parts = msg.split()
        grams = 0
        if len(parts) >= 2 and parts[1].isdigit():
            grams = int(parts[1])
        else:
            publish_event(json.dumps({"type": "error", "message": "Invalid FEED command. Usage: FEED <grams>"}))
            return

        ok, reason = device.can_dispense(grams)
        if ok:
            device.dispense(grams)
            event = {
                "type": "feed",
                "grams": grams,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "remaining_g": device.remaining_g,
                "result": "success",
            }
            append_log(action="FEED", grams=grams, result="success")
            publish_event(json.dumps(event))
        else:
            event = {
                "type": "feed",
                "grams": grams,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "remaining_g": device.remaining_g,
                "result": f"failed: {reason}",
            }
            append_log(action="FEED", grams=grams, result=f"failed: {reason}")
            publish_event(json.dumps(event))
        return

    if msg.upper().startswith("STATUS"):
        summary = device.status_summary()
        event = {"type": "status", **summary}
        publish_event(json.dumps(event))
        return

    publish_event(json.dumps({"type": "error", "message": f"Unknown command: {msg}"}))
