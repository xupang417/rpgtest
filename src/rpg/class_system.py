from dataclasses import dataclass
from src.rpg.stats import Stats


@dataclass
class JobClass:
    id: str
    name: str
    move: int
    growth_hp: int
    growth_str: int
    growth_mag: int
    growth_skl: int
    growth_spd: int
    growth_lck: int
    growth_def: int
    growth_res: int
    allowed_weapons: list[str]


def build_default_classes() -> dict[str, JobClass]:
    return {
        "lord": JobClass(
            id="lord", name="领主", move=5,
            growth_hp=70, growth_str=55, growth_mag=20, growth_skl=60, growth_spd=60, growth_lck=55, growth_def=40, growth_res=30,
            allowed_weapons=["sword"],
        ),
        "knight": JobClass(
            id="knight", name="骑士", move=4,
            growth_hp=80, growth_str=50, growth_mag=10, growth_skl=45, growth_spd=30, growth_lck=35, growth_def=60, growth_res=20,
            allowed_weapons=["lance"],
        ),
        "archer": JobClass(
            id="archer", name="弓手", move=5,
            growth_hp=65, growth_str=50, growth_mag=10, growth_skl=65, growth_spd=55, growth_lck=45, growth_def=30, growth_res=25,
            allowed_weapons=["bow"],
        ),
        "fighter": JobClass(
            id="fighter", name="战士", move=5,
            growth_hp=75, growth_str=60, growth_mag=5, growth_skl=45, growth_spd=50, growth_lck=30, growth_def=35, growth_res=15,
            allowed_weapons=["axe"],
        ),
    }