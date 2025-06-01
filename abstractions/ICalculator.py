from abc import ABC, abstractmethod
from typing import Literal, Tuple, List, Any, Optional
import numpy as np

class ICalculator(ABC):
    @abstractmethod
    def find_cartesian_from_polar(self, r: Literal["R1", "R2"], theta: float) -> Tuple[float, float]: ...

    @abstractmethod
    def find_line_params(self, x1: float, y1: float, x2: float, y2: float) -> Tuple[float, float]: ...

    @abstractmethod
    def get_more_points_from_params(self, k: float, b: float, central_point: Tuple[float, float], scale: float = 5, point_number: int = 100) -> np.ndarray[Any, np.dtype[np.floating[Any]]]: ...

    @abstractmethod
    def find_intersection_point_of_two_lines(self, first_line_params: Tuple[float, float], second_line_params: Tuple[float, float], k_epsilon = 0.2) -> Optional[Tuple[float, float]]: ...

    @abstractmethod
    def find_all_intersection_points(self, k_epsilon = 0.2) -> List[Tuple[float, float]]: ...

    @abstractmethod
    def find_source(self) -> Tuple[float, float]: ...