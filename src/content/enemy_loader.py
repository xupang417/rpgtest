import json
from pathlib import Path


def load_enemy_templates(path: str = "data/enemies/enemy_templates.json") -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    raw = json.loads(p.read_text(encoding="utf-8"))
    result = {}
    for e in raw.get("enemies", []):
        result[e["id"]] = e
    return result