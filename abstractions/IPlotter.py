from abc import ABC, abstractmethod
from numpy.typing import ArrayLike
from typing import Optional, Tuple

class IPlotter(ABC):
    @abstractmethod
    def add_points(self, 
                  x_arr: ArrayLike, 
                  y_arr: ArrayLike,
                  central_point: Optional[Tuple[float, float]] = None,
                  line_style: str = "--k",
                  point_style: dict = {'color': 'red', 's': 100}
                  ) -> None: ...

    @abstractmethod
    def highlight_intersection_points(self) -> None: ...

    @abstractmethod
    def highlight_source(self) -> None: ...

    @abstractmethod
    def finalize(self, title: str) -> None: ...

    @abstractmethod
    def _update_limits(self) -> None: ...