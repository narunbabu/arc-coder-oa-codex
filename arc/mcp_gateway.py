"""MCP gateway exposing workers over stdio."""
from __future__ import annotations

import json
import sys
from typing import Callable, Dict


class MCPGateway:
    """Expose callable workers over stdio using JSON lines."""

    def __init__(self, handlers: Dict[str, Callable[..., object]]) -> None:
        self.handlers = handlers

    def serve(self) -> None:
        """Serve requests forever."""
        for line in sys.stdin:
            req = json.loads(line)
            method = req.get("method")
            handler = self.handlers.get(method)
            if handler is None:
                continue
            result = handler(*req.get("args", []))
            sys.stdout.write(json.dumps(result) + "\n")
            sys.stdout.flush()
