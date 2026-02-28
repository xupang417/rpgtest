import json
from pathlib import Path


def load_dialogue(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def load_chapter_dialogues(chapter_id: str, base_dir: str = "data/dialogues") -> dict:
    file_name = f"{chapter_id}_dialogues.json"
    return load_dialogue(str(Path(base_dir) / file_name))
