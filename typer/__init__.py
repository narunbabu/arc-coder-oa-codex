from __future__ import annotations

from typing import Any, Callable, Optional
from pathlib import Path
import inspect
import click
from click.testing import CliRunner as _CliRunner


def echo(message: str) -> None:
    click.echo(message)

class Typer:
    def __init__(self, help: Optional[str] = None) -> None:
        self.cli = click.Group(help=help)

    def command(self, *args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
            params: list[click.Parameter] = []
            sig = inspect.signature(func)
            for name, param in sig.parameters.items():
                ann = param.annotation
                if ann is bool or ann == "bool":
                    params.append(click.Option([f"--{name}"], is_flag=True))
                else:
                    click_type = click.Path(path_type=Path) if ann in (Path, "Path") else None
                    params.append(click.Argument([name], type=click_type))
            cmd = click.Command(func.__name__, callback=func, params=params, help=func.__doc__)
            self.cli.add_command(cmd)
            return func

        return wrapper

    def __call__(self, argv: list[str]) -> Any:
        self.cli.main(args=argv, prog_name=self.cli.name, standalone_mode=False)

    def main(self, argv: Optional[list[str]] = None) -> Any:
        self.cli.main(args=argv, prog_name=self.cli.name, standalone_mode=False)

    def echo(self, message: str) -> None:
        click.echo(message)


class CliRunner(_CliRunner):
    pass
