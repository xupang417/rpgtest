import random
from src.battle.hit_formula import calc_hit
from src.battle.crit_formula import calc_crit
from src.battle.damage_formula import calc_damage


def resolve_basic_attack(attacker, defender, terrain_defender):
    """
    attacker/defender: Unit
    """
    hit_rate = calc_hit(attacker, defender, terrain_defender)
    roll = random.randint(1, 100)
    if roll > hit_rate:
        return {"hit": False, "crit": False, "damage": 0, "defeated": False}

    crit_rate = calc_crit(attacker, defender)
    is_crit = random.randint(1, 100) <= crit_rate

    dmg = calc_damage(attacker, defender, terrain_defender)
    if is_crit:
        dmg *= 3

    defender.hp -= dmg
    defeated = defender.hp <= 0
    if defeated:
        defender.hp = 0
        defender.alive = False

    return {"hit": True, "crit": is_crit, "damage": dmg, "defeated": defeated}