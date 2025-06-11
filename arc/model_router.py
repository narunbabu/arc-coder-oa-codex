"""Model router selecting models under rate limits."""
from __future__ import annotations

import yaml  # type: ignore
from pathlib import Path
from typing import Dict

from .rate_limiter import Quota, RateLimiter


class ModelRouter:
    """Routes steps to models based on quotas."""

    def __init__(self, registry_path: Path, limiter: RateLimiter) -> None:
        self.registry_path = registry_path
        self.limiter = limiter
        self.models: Dict[str, Quota] = {}
        data = yaml.safe_load(registry_path.read_text())
        for name, values in data.items():
            self.models[name] = Quota(rpm=values.get("rpm", 0), rpd=values.get("rpd"))

    def choose_model(self, key: str) -> str:
        """Return the first model that is under quota."""
        for name, quota in self.models.items():
            if self.limiter.allow(f"{key}:{name}", quota):
                return name
        raise RuntimeError("No model available")
