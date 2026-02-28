import random
from src.rpg.unit import Unit


def try_level_up(unit: Unit):
    while unit.exp >= 100:
        unit.exp -= 100
        unit.level += 1
        jc = unit.job

        if random.randint(1, 100) <= jc.growth_hp:
            unit.max_hp += 1
            unit.hp += 1
        if random.randint(1, 100) <= jc.growth_str:
            unit.base.str_ += 1
        if random.randint(1, 100) <= jc.growth_mag:
            unit.base.mag += 1
        if random.randint(1, 100) <= jc.growth_skl:
            unit.base.skl += 1
        if random.randint(1, 100) <= jc.growth_spd:
            unit.base.spd += 1
        if random.randint(1, 100) <= jc.growth_lck:
            unit.base.lck += 1
        if random.randint(1, 100) <= jc.growth_def:
            unit.base.def_ += 1
        if random.randint(1, 100) <= jc.growth_res:
            unit.base.res += 1