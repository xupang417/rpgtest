def calc_damage(attacker, defender, terrain_defender):
    atk = attacker.str_ + attacker.might
    d = atk - (defender.def_ + terrain_defender.defense)
    return max(0, d)