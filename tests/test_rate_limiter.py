from arc.rate_limiter import Quota, RateLimiter


def test_rate_limiter_allows() -> None:
    limiter = RateLimiter("redis://localhost:6379/1")
    limiter.redis.flushdb()
    q = Quota(rpm=2, rpd=4)
    assert limiter.allow("test", q)
    assert limiter.allow("test", q)
    assert not limiter.allow("test", q)
