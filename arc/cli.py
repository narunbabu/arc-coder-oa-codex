"""arc command line interface.

Usage:
  arc run [OPTIONS] PLAN
  arc status
  arc resume
  arc config
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional
import sys

import typer

from .browser_worker import run_browser_task
from .plan_loader import load_plan

app = typer.Typer(help=__doc__)


def _run_plan(plan_path: Path, no_docker: bool = False) -> None:
    steps = load_plan(plan_path)
    screenshots = Path("screenshots")
    screenshots.mkdir(exist_ok=True)
    for i, step in enumerate(steps, 1):
        outfile = screenshots / f"step-{i}.png"
        run_browser_task(outfile)
        typer.echo(f"Completed {step}")
        typer.echo(f"Screenshot saved to {outfile}")


@app.command()
def run(plan: Path, no_docker: bool = False) -> None:
    """Run a plan file."""
    _run_plan(plan, no_docker=no_docker)


@app.command()
def status() -> None:
    """Show status (stub)."""
    typer.echo("OK")


@app.command()
def resume() -> None:
    """Resume a plan (stub)."""
    typer.echo("Resumed")


@app.command()
def config() -> None:
    """Show config (stub)."""
    typer.echo("Config loaded")


def main(argv: Optional[list[str]] = None) -> None:
    """Entry point for console script."""
    args = argv if argv is not None else sys.argv[1:]
    app.main(args)


if __name__ == "__main__":  # pragma: no cover
    main()
