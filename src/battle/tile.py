from dataclasses import dataclass


@dataclass
class TileDef:
    id: str
    move_cost: int
    avoid: int
    defense: int
    color: tuple[int, int, int]

