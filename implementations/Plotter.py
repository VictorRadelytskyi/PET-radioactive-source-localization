from PET_radioactive_source_localization.abstractions.IPlotter import IPlotter
from PET_radioactive_source_localization.implementations.DataHolder import DataHolder
from numpy.typing import ArrayLike
import matplotlib.pyplot as plt
from typing import Optional, Tuple, Dict, List
import numpy as np

class Plotter(IPlotter):
    def __init__(self, dataholder: DataHolder) -> None:
        self.dataholder: DataHolder = dataholder
        self.fig, self.ax = plt.subplots()
        self._initialize_plot_settings()

    def _initialize_plot_settings(self) -> None:
        """Initialize default plot settings"""
        self.default_line_style = "--k"
        self.default_point_style = {'color': 'red', 's': 100}
        self.intersection_style = {'color': 'blue', 's': 80, 'label': 'Intersections'}
        self.source_style = {'color': 'orange', 's': 120, 'label': 'Source'}
        self.intersection_points_uncertainty_style = {
            'fmt': 'o',
            'capsize': 3,
            'capthick': 1,
            'elinewidth': 1,
            'alpha': 0.7
        }
        self.source_point_uncertainty_style = {
            'capsize': 3,
            'capthick': 1,
            'elinewidth': 1,
            'alpha': 0.7,
            'color': 'orange'
        }

    def add_points(self, 
                  x_arr: ArrayLike, 
                  y_arr: ArrayLike,
                  central_point: Optional[Tuple[float, float]] = None,
                  uncertainties: Optional[Tuple[ArrayLike, ArrayLike]] = None,
                  line_style: Optional[str] = None,
                  point_style: Optional[Dict] = None
                  ) -> None:
        """
        Add new points to the plot with optional uncertainties
        
        Args:
            x_arr: X-coordinates
            y_arr: Y-coordinates
            central_point: Optional (x,y) to highlight
            uncertainties: Tuple of (x_uncertainties, y_uncertainties)
            line_style: Matplotlib line specification
            point_style: kwargs for scatter plot
        """
        line_style = line_style or self.default_line_style
        point_style = point_style or self.default_point_style
        
        self._update_data_arrays(x_arr, y_arr)
        
        
        self.ax.plot(x_arr, y_arr, line_style)
        
        if uncertainties:
            u_x, u_y = uncertainties
            self.ax.errorbar(
                x_arr, y_arr,
                xerr=u_x,
                yerr=u_y,
                **self.intersection_points_uncertainty_style
            )
        
        # Mark central point if provided
        if central_point:
            self.ax.scatter(central_point[0], central_point[1], **point_style)
        
        self._update_limits()

    def _update_data_arrays(self, x_arr: ArrayLike, y_arr: ArrayLike) -> None:
        """Update stored data arrays with new points"""
        self.dataholder.all_x = list(np.concatenate([self.dataholder.all_x, np.array(x_arr)]))
        self.dataholder.all_y = list(np.concatenate([self.dataholder.all_y, np.array(y_arr)]))

    def highlight_intersection_points(self, show_uncertainties: bool = True) -> None:
        """Plot intersection points with optional uncertainties"""
        if not self.dataholder.intersection_points:
            return
            
        x, y = zip(*self.dataholder.intersection_points)
        self.ax.scatter(x, y, **self.intersection_style)
        
        if show_uncertainties and hasattr(self.dataholder, 'u_intersection_points'):
            u_x, u_y = zip(*self.dataholder.u_intersection_points)
            self.ax.errorbar(
                x, y,
                xerr=u_x,
                yerr=u_y,
                **self.intersection_points_uncertainty_style
            )

    def highlight_source(self, show_uncertainty: bool = False) -> None:
        """Highlight the source location"""
        if not self.dataholder.source:
            raise ValueError("Cannot highlight source - no source attribute found")
        
        self.ax.scatter(
            self.dataholder.source[0], 
            self.dataholder.source[1],
            **self.source_style
        )

        if show_uncertainty:
            if len(self.dataholder.u_source) == 0:
                raise ValueError(f'No uncertainty found for the source: {self.dataholder.u_source}')
            self.ax.errorbar(
                self.dataholder.source[0],
                self.dataholder.source[1],
                xerr = self.dataholder.u_source[0],
                yerr = self.dataholder.u_source[1],
                **self.source_point_uncertainty_style
            )

    def _update_limits(self, padding_factor: float = 0.1) -> None:
        """Adjust axes limits to fit all data with padding"""
        if not self.dataholder.all_x:
            return
            
        x_min, x_max = np.min(self.dataholder.all_x), np.max(self.dataholder.all_x)
        y_min, y_max = np.min(self.dataholder.all_y), np.max(self.dataholder.all_y)
        
        x_pad = padding_factor * (x_max - x_min)
        y_pad = padding_factor * (y_max - y_min)
        
        self.ax.set_xlim(x_min - x_pad, x_max + x_pad)
        self.ax.set_ylim(y_min - y_pad, y_max + y_pad)

    def finalize(self, title: str = "Cumulative Plot", save: bool = False, filepath: Optional[str] = None) -> None:
        """Add finishing touches and show plot"""
        self.ax.grid(True, linestyle='--', alpha=0.5)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_title(title)
        self.ax.legend()
        plt.tight_layout()
        if save:
            if not filepath: 
                raise ValueError(f'can\'t save figure, because no filepath is provided: {filepath}')
            
        plt.show()