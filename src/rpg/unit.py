from dataclasses import dataclass
from src.rpg.stats import Stats


@dataclass
class Unit:
    id: str
    name: str
    team: str
    x: int
    y: int
    job: object
    base: Stats
    weapon: object
    level: int = 1
    alive: bool = True
    acted: bool = False

    def __post_init__(self):
        self.max_hp = self.base.hp
        self.hp = self.base.hp
        self.str_ = self.base.str_
        self.mag = self.base.mag
        self.skl = self.base.skl
        self.spd = self.base.spd
        self.lck = self.base.lck
        self.def_ = self.base.def_
        self.res = self.base.res
        self.might = getattr(self.weapon, "might", 0)
        self.hit = getattr(self.weapon, "hit", 0)
        self.crit = getattr(self.weapon, "crit", 0)
        self.range_min = getattr(self.weapon, "range_min", 1)
        self.range_max = getattr(self.weapon, "range_max", 1)

