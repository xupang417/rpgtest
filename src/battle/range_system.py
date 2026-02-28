def in_attack_range(ax: int, ay: int, bx: int, by: int, rmin: int, rmax: int) -> bool:
    d = abs(ax - bx) + abs(ay - by)
    return rmin <= d <= rmax