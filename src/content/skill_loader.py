import json
from pathlib import Path
from src.rpg.skill import Skill


def load_skills(path: str = "data/skills/active_skills.json") -> dict[str, Skill]:
    p = Path(path)
    if not p.exists():
        return {}

    raw = json.loads(p.read_text(encoding="utf-8"))
    result: dict[str, Skill] = {}

    for s in raw.get("skills", []):
        obj = Skill(
            id=s["id"],
            name=s["name"],
            kind=s["kind"],
            power=s.get("power", 1.0),
            range_min=s["range"][0],
            range_max=s["range"][1],
            cost=s.get("cost", 0),
            status=s.get("status"),
            status_turns=s.get("status_turns", 0),
        )
        result[obj.id] = obj

    return result