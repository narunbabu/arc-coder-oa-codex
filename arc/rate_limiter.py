"""Simple token-bucket rate limiter backed by Redis."""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional, List, cast

import redis


@dataclass
class Quota:
    """Rate limit quota."""

    rpm: int
    rpd: Optional[int] = None


class RateLimiter:
    """Token bucket rate limiter supporting rpm and rpd."""

    def __init__(self, redis_url: str = "redis://localhost:6379/0") -> None:
        self.redis = redis.Redis.from_url(redis_url, decode_responses=True)

    def allow(self, key: str, quota: Quota) -> bool:
        """Return True if the action is allowed under quota."""
        now = int(time.time())
        minute = now // 60
        day = now // 86400
        pipe = self.redis.pipeline()
        pipe.hincrby(key, f"m:{minute}", 1)
        pipe.expire(key, 86400)
        if quota.rpd is not None:
            pipe.hincrby(key, f"d:{day}", 1)
        counts = cast(List[Optional[int]], pipe.execute())
        minute_count = int(counts[0] or 0)
        if minute_count > quota.rpm:
            return False
        if quota.rpd is not None:
            day_count = int(counts[2] or 0)
            if day_count > quota.rpd:
                return False
        return True
