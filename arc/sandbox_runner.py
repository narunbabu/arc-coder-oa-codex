"""Run commands in a sandbox using Docker when available."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable, List


def run_in_sandbox(cmd: Iterable[str], workdir: Path, use_docker: bool = True) -> None:
    """Execute a command optionally inside Docker."""
    if use_docker:
        docker_cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{workdir}:/work",
            "-w",
            "/work",
            "python:3.12",
        ] + list(cmd)
        subprocess.run(docker_cmd, check=True)
    else:
        subprocess.run(list(cmd), cwd=workdir, check=True)
