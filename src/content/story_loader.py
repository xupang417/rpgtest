import json
from pathlib import Path


def load_main_story(path: str = "data/story/main_story.json") -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    raw = json.loads(p.read_text(encoding="utf-8"))
    return raw.get("story", {})