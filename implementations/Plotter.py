from PET_radioactive_source_localization.abstractions.IPlotter import IPlotter
from PET_radioactive_source_localization.implementations.DataHolder import DataHolder
from numpy.typing import ArrayLike
import matplotlib.pyplot as plt
from typing import Optional, Tuple


class Plotter(IPlotter):
    def __init__(self, dataholder: DataHolder) -> None:
        self.dataholder: DataHolder = dataholder
        self.fig, self.ax = plt.subplots()


    def add_points(self, 
                  x_arr: ArrayLike, 
                  y_arr: ArrayLike,
                  central_point: Optional[Tuple[float, float]] = None,
                  line_style: str = "--k",
                  point_style: dict = {'color': 'red', 's': 100}
                  ) -> None:
        """
        Add new points to the cumulative plot
        
        Args:
            x_arr: New x-coordinates
            y_arr: New y-coordinates  
            central_point: Optional (x,y) to highlight
            line_style: Matplotlib line specification
            point_style: kwargs for scatter plot
        """
        # Store all points for auto-scaling
        self.dataholder.all_x.extend(x_arr) # type: ignore
        self.dataholder.all_y.extend(y_arr) # type: ignore
        
        # Plot the new segment
        self.ax.plot(x_arr, y_arr, line_style)
        
        # Mark central point if provided
        if central_point:
            self.ax.scatter(central_point[0], central_point[1], **point_style)
        
        # Auto-scale to all data
        self._update_limits()
        
    def _update_limits(self) -> None:
        """Adjust axes limits to fit all data with 10% padding"""
        x_min, x_max = min(self.dataholder.all_x), max(self.dataholder.all_x)
        y_min, y_max = min(self.dataholder.all_y), max(self.dataholder.all_y)
        
        x_pad = 0.1 * (x_max - x_min)
        y_pad = 0.1 * (y_max - y_min)
        
        self.ax.set_xlim(x_min - x_pad, x_max + x_pad)
        self.ax.set_ylim(y_min - y_pad, y_max + y_pad)
    
    def highlight_intersection_points(self) -> None:
        for x, y in self.dataholder.intersection_points:
            self.ax.scatter(x = x, y = y, color="blue")

    def highlight_source(self) -> None:
        if not self.dataholder.source:
            raise ValueError("Can\'t highlight source, because no source attribute was found")
        self.ax.scatter(self.dataholder.source[0], self.dataholder.source[1], color ="orange", label = "source")

    def finalize(self, title: str = "Cumulative Plot") -> None:
        """Add finishing touches and show plot"""
        self.ax.grid(True, linestyle='--', alpha=0.5)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_title(title)
        plt.show()