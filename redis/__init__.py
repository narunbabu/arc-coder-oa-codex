from __future__ import annotations

from collections import defaultdict
from typing import Dict


class RedisPipeline:
    def __init__(self, redis: 'Redis') -> None:
        self.redis = redis
        self.commands: list[tuple] = []

    def hincrby(self, key: str, field: str, amount: int) -> None:
        self.commands.append(("hincrby", key, field, amount))

    def expire(self, key: str, ttl: int) -> None:
        self.commands.append(("expire", key, ttl))

    def execute(self) -> list[int | None]:
        results: list[int | None] = []
        for cmd in self.commands:
            if cmd[0] == "hincrby":
                _, key, field, amount = cmd
                val = self.redis.hincrby(key, field, amount)
                results.append(val)
            elif cmd[0] == "expire":
                _, key, ttl = cmd
                self.redis.expire(key, ttl)
                results.append(None)
        return results


class Redis:
    def __init__(self) -> None:
        self.store: Dict[str, Dict[str, int]] = defaultdict(dict)

    @classmethod
    def from_url(cls, url: str, decode_responses: bool = True) -> 'Redis':
        return cls()

    def pipeline(self) -> 'RedisPipeline':
        return RedisPipeline(self)

    def hincrby(self, key: str, field: str, amount: int) -> int:
        self.store[key][field] = self.store[key].get(field, 0) + amount
        return self.store[key][field]

    def expire(self, key: str, ttl: int) -> None:
        pass

    def flushdb(self) -> None:
        self.store.clear()
