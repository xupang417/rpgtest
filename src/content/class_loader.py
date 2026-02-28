import json
from pathlib import Path
from src.rpg.class_system import JobClass


def load_classes(path: str = "data/classes/classes.json") -> dict[str, JobClass]:
    p = Path(path)
    if not p.exists():
        return {}

    raw = json.loads(p.read_text(encoding="utf-8"))
    result: dict[str, JobClass] = {}

    for c in raw.get("classes", []):
        jc = JobClass(
            id=c["id"],
            name=c["name"],
            move=c["move"],
            growth_hp=c["growth"]["hp"],
            growth_str=c["growth"]["str"],
            growth_mag=c["growth"]["mag"],
            growth_skl=c["growth"]["skl"],
            growth_spd=c["growth"]["spd"],
            growth_lck=c["growth"]["lck"],
            growth_def=c["growth"]["def"],
            growth_res=c["growth"]["res"],
            allowed_weapons=c.get("allowed_weapons", []),
        )
        result[jc.id] = jc

    return result