from pathlib import Path

from arc.plan_loader import load_plan


def test_load_plan(tmp_path: Path) -> None:
    f = tmp_path / "plan.md"
    f.write_text("- step1\n- step2")
    assert load_plan(f) == ["step1", "step2"]
