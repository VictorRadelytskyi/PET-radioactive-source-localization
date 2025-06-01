from dataclasses import dataclass, field
from typing import List, Tuple, Optional

@dataclass
class DataHolder:
    all_x: List[float]  = field(default_factory=list)
    all_y: List[float] = field(default_factory=list)
    all_lines_params: List[Tuple[float, float]] = field(default_factory=list)
    R1: float = 15
    R2: float = 11
    uR1: float = 1
    uR2: float = 1
    intersection_points: List[Tuple[float, float]] = field(default_factory=list)
    source: Optional[Tuple[float, float]] = None