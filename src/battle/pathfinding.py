from collections import deque


def manhattan(ax: int, ay: int, bx: int, by: int) -> int:
    return abs(ax - bx) + abs(ay - by)


def reachable_tiles(start_x, start_y, move_points, grid, blocked: set[tuple[int, int]]):
    """
    简化版可达格：按地形消耗BFS，返回可达坐标集合（不含起点）
    """
    q = deque()
    q.append((start_x, start_y, move_points))
    visited = {(start_x, start_y): move_points}
    result = set()

    while q:
        x, y, remain = q.popleft()
        for nx, ny in grid.neighbors4(x, y):
            if (nx, ny) in blocked and (nx, ny) != (start_x, start_y):
                continue
            cost = grid.tile_def(nx, ny).move_cost
            nr = remain - cost
            if nr < 0:
                continue
            if (nx, ny) not in visited or visited[(nx, ny)] < nr:
                visited[(nx, ny)] = nr
                q.append((nx, ny, nr))
                if (nx, ny) != (start_x, start_y):
                    result.add((nx, ny))
    return result