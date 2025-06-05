from abc import ABC, abstractmethod
from numpy.typing import ArrayLike
from typing import Optional, Tuple, Dict

class IPlotter(ABC):
    @abstractmethod
    def add_points(self, 
                  x_arr: ArrayLike, 
                  y_arr: ArrayLike,
                  central_point: Optional[Tuple[float, float]] = None,
                  uncertainties: Optional[Tuple[ArrayLike, ArrayLike]] = None,
                  line_style: Optional[str] = None,
                  point_style: Optional[Dict] = None
                  ) -> None: ...

    @abstractmethod
    def highlight_intersection_points(self, show_uncertainties: bool = False) -> None: ...

    @abstractmethod
    def highlight_source(self, show_uncertainty: bool = False) -> None: ...

    @abstractmethod
    def finalize(self, title: str) -> None: ...

    @abstractmethod
    def _update_limits(self) -> None: ...