import json
from pathlib import Path


SAVE_DIR = Path("saves")
SAVE_DIR.mkdir(parents=True, exist_ok=True)


def save_game(slot: int, data: dict):
    path = SAVE_DIR / f"slot_{slot}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_game(slot: int):
    path = SAVE_DIR / f"slot_{slot}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))