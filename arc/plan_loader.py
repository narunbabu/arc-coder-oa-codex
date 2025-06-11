"""Plan loader for arc-coder.

Parses a markdown plan file into a list of textual steps.
"""
from __future__ import annotations

from pathlib import Path
from typing import List


def load_plan(path: Path) -> List[str]:
    """Load a plan file and return step strings."""
    lines = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith("-"):
            lines.append(line.lstrip("- "))
    return lines
