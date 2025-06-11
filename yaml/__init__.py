from typing import Any, Dict


def safe_load(s: str) -> Any:
    data: Dict[str, Dict[str, int]] = {}
    if not s.strip():
        return data
    current_key = None
    for line in s.splitlines():
        if line.startswith(' '):
            if current_key is None:
                continue
            k, v = line.strip().split(':')
            data[current_key][k] = int(v.strip())
        else:
            current_key = line.rstrip(':')
            data[current_key] = {}
    return data

