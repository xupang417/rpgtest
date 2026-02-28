def calc_hit(attacker, defender, terrain_defender):
    base_hit = attacker.hit + attacker.skl * 2 + attacker.lck
    avoid = defender.spd * 2 + defender.lck + terrain_defender.avoid
    return max(5, min(95, base_hit - avoid))