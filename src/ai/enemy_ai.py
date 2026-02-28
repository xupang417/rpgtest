from src.battle.pathfinding import manhattan


class EnemyAI:
    """
    简化策略：
    1) 如果能打到玩家，打血量最低的
    2) 否则往最近玩家靠近
    """
    def choose(self, enemy, players, occupied, grid):
        if not players:
            return ("wait", None)

        attackable = []
        for p in players:
            d = manhattan(enemy.x, enemy.y, p.x, p.y)
            if enemy.range_min <= d <= enemy.range_max:
                attackable.append(p)
        if attackable:
            attackable.sort(key=lambda u: u.hp)
            return ("attack", attackable[0])

        target = min(players, key=lambda p: manhattan(enemy.x, enemy.y, p.x, p.y))
        ex, ey = enemy.x, enemy.y
        candidates = [(ex + 1, ey), (ex - 1, ey), (ex, ey + 1), (ex, ey - 1)]

        best = (ex, ey)
        best_d = manhattan(ex, ey, target.x, target.y)

        for nx, ny in candidates:
            if not grid.in_bounds(nx, ny):
                continue
            if (nx, ny) in occupied:
                continue
            d = manhattan(nx, ny, target.x, target.y)
            if d < best_d:
                best_d = d
                best = (nx, ny)

        if best != (ex, ey):
            return ("move", best)
        return ("wait", None)