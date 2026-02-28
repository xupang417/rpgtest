import json
from pathlib import Path


def load_promotions(path: str = "data/classes/promotions.json") -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    raw = json.loads(p.read_text(encoding="utf-8"))
    return raw.get("promotions", [])