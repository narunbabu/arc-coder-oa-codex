from pathlib import Path

from arc.model_router import ModelRouter
from arc.rate_limiter import Quota, RateLimiter


def test_choose_model(tmp_path: Path) -> None:
    registry = tmp_path / "models.yaml"
    registry.write_text("a:\n  rpm: 1\n")
    limiter = RateLimiter("redis://localhost:6379/1")
    limiter.redis.flushdb()
    router = ModelRouter(registry, limiter)
    assert router.choose_model("u") == "a"
