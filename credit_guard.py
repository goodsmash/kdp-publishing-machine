#!/usr/bin/env python3
import json, os
from datetime import datetime

STATE_FILE = "/home/goodsmash/.openclaw/workspace/kdp-publishing-machine/.credits_state.json"

class CreditGuard:
    def __init__(self):
        # User policy: use only half of free credits
        self.daily_free_estimate = int(os.getenv("DAILY_FREE_CREDITS_ESTIMATE", "100"))
        self.safe_fraction = float(os.getenv("SAFE_CREDIT_FRACTION", "0.5"))
        self.max_images = int(self.daily_free_estimate * self.safe_fraction)
        self.state = self._load()

    def _today(self):
        return datetime.now().strftime("%Y-%m-%d")

    def _load(self):
        if not os.path.exists(STATE_FILE):
            return {"date": self._today(), "images_used": 0}
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            data = {"date": self._today(), "images_used": 0}
        if data.get("date") != self._today():
            data = {"date": self._today(), "images_used": 0}
        return data

    def _save(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=2)

    def can_spend(self, amount=1):
        return (self.state.get("images_used", 0) + amount) <= self.max_images

    def spend(self, amount=1):
        self.state["images_used"] = self.state.get("images_used", 0) + amount
        self._save()

    def summary(self):
        used = self.state.get("images_used", 0)
        return {
            "date": self.state.get("date"),
            "used": used,
            "cap": self.max_images,
            "remaining": max(0, self.max_images - used)
        }

if __name__ == "__main__":
    g = CreditGuard()
    print(g.summary())
