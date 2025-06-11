"""Interface to the Codex CLI."""
from __future__ import annotations

import json
import subprocess
from typing import Any, Dict


def run_codex(payload: Dict[str, Any]) -> str:
    """Run the Codex CLI with the given payload."""
    result = subprocess.run(
        ["codex"],
        check=True,
        input=json.dumps(payload).encode(),
        capture_output=True,
    )
    return result.stdout.decode()
