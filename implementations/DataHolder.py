from dataclasses import dataclass, field
from typing import List, Tuple, Optional

@dataclass
class DataHolder:
    """
    A class that will store all computed data, which IPlotter and ICalculator will have access to
    Conventions: u=sqrt(U^2+S^2) represents the total uncertainity as a euclidian 
    norm of systematic uncertainity U and statistical uncertainity S (sigma) 
    Conventions: uncertainities for variable ${var} are written with prefix [u|U|S]_${var}
    calculator.find_uncertainity_of_composed_function(self, f: Callable) will use that convention to calculate uncertainities
    """
    
    thetas: List[Tuple[float, float]] = field(default_factory=list)
    S_thetas: Optional[List[Tuple[float, float]]] = None
    U_thetas: float = 0.5
    u_thetas: Optional[List[Tuple[float, float]]] = None

    R1: float = 15
    R2: float = 11
    u_R1: float = 0.5 
    u_R2: float = 0.5

    points: List[Tuple[Tuple[float, float], Tuple[float, float]]] = field(default_factory=list) # all pairs of points, that were used to find line equations
    u_points: List[Tuple[Tuple[float, float], Tuple[float, float]]] = field(default_factory=list) 

    all_lines_params: List[Tuple[float, float]] = field(default_factory=list)
    u_all_lines_params: List[Tuple[float, float]] = field(default_factory=list)

    intersection_points: List[Tuple[float, float]] = field(default_factory=list)
    u_intersection_points: List[Tuple[float, float]] = field(default_factory=list)

    source: Optional[Tuple[float, float]] = None
    u_source: Tuple[float, float] = field(default_factory=tuple)

    all_x: List[float]  = field(default_factory=list) # all x coordinates generated on some line for matplotlib.pyplot drawings. Not to confuse with points used to find lines parameters
    all_y: List[float] = field(default_factory=list)
