from dataclasses import dataclass
from typing import Optional


@dataclass
class Skill:
    id: str
    name: str
    kind: str
    power: float
    range_min: int
    range_max: int
    cost: int = 0
    status: Optional[str] = None
    status_turns: int = 0
