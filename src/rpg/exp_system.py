def exp_for_attack(hit: bool, defeated: bool) -> int:
    if defeated:
        return 40
    if hit:
        return 15
    return 8