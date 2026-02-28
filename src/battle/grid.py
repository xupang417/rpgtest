from __future__ import annotations
from src.battle.tile import TileDef


TERRAIN_DB: dict[str, TileDef] = {
    "plain": TileDef("plain", move_cost=1, avoid=0, defense=0, color=(96, 168, 96)),
    "forest": TileDef("forest", move_cost=2, avoid=20, defense=1, color=(56, 120, 56)),
    "mountain": TileDef("mountain", move_cost=3, avoid=30, defense=2, color=(120, 120, 120)),
    "fort": TileDef("fort", move_cost=1, avoid=10, defense=2, color=(160, 140, 90)),
}


class GridMap:
    def __init__(self, width: int = 12, height: int = 8):
        self.w = width
        self.h = height
        self.tiles: list[list[str]] = [["plain" for _ in range(self.w)] for _ in range(self.h)]

    def apply_terrain_overrides(self, overrides: list[dict]):
        for obj in overrides:
            x, y = obj["x"], obj["y"]
            terrain = obj["terrain"]
            if self.in_bounds(x, y) and terrain in TERRAIN_DB:
                self.tiles[y][x] = terrain

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.w and 0 <= y < self.h

    def neighbors4(self, x: int, y: int):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny):
                yield nx, ny

    def tile_def(self, x: int, y: int) -> TileDef:
        return TERRAIN_DB[self.tiles[y][x]]