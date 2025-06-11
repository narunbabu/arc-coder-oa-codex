from pathlib import Path

from typer.testing import CliRunner

from arc.cli import app


def test_cli_run(tmp_path: Path) -> None:
    plan = tmp_path / "p.md"
    plan.write_text("- hi")
    runner = CliRunner()
    result = runner.invoke(app.cli, ["run", str(plan)])
    assert result.exit_code == 0
