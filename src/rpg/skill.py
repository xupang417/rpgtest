from dataclasses import dataclass


@dataclass
class Skill:
    id: str
    name: str
    kind: str
    power: float
    range_min: int
    range_max: int
    cost: int = 0
    status: str | None = None
    status_turns: int = 0

