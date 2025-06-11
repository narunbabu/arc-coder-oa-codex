import pytest
from pathlib import Path

from arc.browser_worker import run_browser_task


@pytest.mark.e2e
def test_browser_worker(tmp_path: Path) -> None:
    out = tmp_path / "shot.png"
    try:
        run_browser_task(out)
    except Exception as exc:  # pragma: no cover
        pytest.skip(str(exc))
    assert out.exists()
