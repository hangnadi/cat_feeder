from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class DeviceState:
    hopper_capacity_g: int = 2000  # total capacity (g)
    remaining_g: int = 2000        # current remaining (g)
    last_feed_at: datetime | None = None
    feeds_today: int = 0
    daily_quota_g: int = 300       # optional daily quota

    def can_dispense(self, grams: int) -> tuple[bool, str]:
        if grams <= 0:
            return False, "Invalid amount"
        if grams > self.remaining_g:
            return False, "Not enough food in hopper"
        # simple daily quota rule
        today = datetime.now().date()
        if self.last_feed_at and self.last_feed_at.date() == today:
            if self.feeds_today * 1 >= 8:  # arbitrary max feeds/day
                return False, "Max feeds for today reached"
        return True, "OK"

    def dispense(self, grams: int) -> None:
        self.remaining_g -= grams
        now = datetime.now()
        if self.last_feed_at and self.last_feed_at.date() == now.date():
            self.feeds_today += 1
        else:
            self.feeds_today = 1
        self.last_feed_at = now

    def status_summary(self) -> dict:
        return {
            "remaining_g": self.remaining_g,
            "last_feed_at": self.last_feed_at.isoformat() if self.last_feed_at else None,
            "feeds_today": self.feeds_today,
        }
