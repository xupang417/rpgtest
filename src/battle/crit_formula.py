def calc_crit(attacker, defender):
    base = attacker.crit + attacker.skl // 2 - defender.lck
    return max(0, min(100, base))