import json
from pathlib import Path
from src.rpg.equipment import Weapon


def load_weapons(path: str = "data/items/weapons.json") -> dict[str, Weapon]:
    p = Path(path)
    if not p.exists():
        return {}

    raw = json.loads(p.read_text(encoding="utf-8"))
    result: dict[str, Weapon] = {}

    for w in raw.get("weapons", []):
        wp = Weapon(
            id=w["id"],
            name=w["name"],
            wtype=w["type"],
            might=w["might"],
            hit=w["hit"],
            crit=w["crit"],
            range_min=w["range"][0],
            range_max=w["range"][1],
        )
        result[wp.id] = wp

    return result