from dataclasses import dataclass


@dataclass
class Weapon:
    id: str
    name: str
    wtype: str
    might: int
    hit: int
    crit: int
    range_min: int
    range_max: int


def can_equip(unit, weapon: Weapon) -> bool:
    return weapon.wtype in unit.job.allowed_weapons