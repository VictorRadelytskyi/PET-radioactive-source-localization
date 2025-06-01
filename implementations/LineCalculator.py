from PET_radioactive_source_localization.abstractions.ICalculator import ICalculator
from PET_radioactive_source_localization.implementations.DataHolder import DataHolder
from typing import List, Tuple, Literal, Any
import numpy as np

class LineCalculator(ICalculator):
    def __init__(self, dataholder: DataHolder):
        self.dataholder = dataholder

    def find_all_intersection_points(self, k_epsilon = 0.2) -> List[Tuple[float, float]]:
        """Find all the intersection points of multiple lines y1=k1x1+b1,...,y_n=k_n*x_n+b_n. It's guaranteed to have (n-1)! solution unless the list contains parallel lines"""
        if len(self.dataholder.all_lines_params) == 0:
            raise ValueError(f'can\'t find intersection point of all lines, because all_lines_params is empty: {self.dataholder.all_lines_params}')
        for i, (k_i, b_i) in enumerate(self.dataholder.all_lines_params[:-1]):
            for (k_j, b_j) in self.dataholder.all_lines_params[i+1:]:
                self.find_intersection_point_of_two_lines((k_i, b_i), (k_j, b_j), k_epsilon = 0.2)
        return self.dataholder.intersection_points 
    
    def find_intersection_point_of_two_lines(self, first_line_params: Tuple[float, float], second_line_params: Tuple[float, float], k_epsilon = 0.2) -> Tuple[float, float] | None:
        """Find intersection of two lines: y1=k1x1+b1 and y2=k2x2+b2. It's guaranteed to have exactly 1 solution unless k1=k2 meaning the lines are parallel"""
        k1, b1 = first_line_params
        k2, b2 = second_line_params
        if np.abs(k2-k1) > k_epsilon:
            x = (b2-b1)/(k1-k2)
            y = (k1*x+b1)/2+(k2*x+b2)/2
            self.dataholder.intersection_points.append((x,y))
            return (x,y)
        
    def find_cartesian_from_polar(self, r: Literal["R1", "R2"], theta: float) -> Tuple[float, float]:
        """get cartesian coordinates of a point, knowing it\'s radius and theta in degrees in polar coordinates"""
        r = getattr(self.dataholder, r) 
        return (r*np.cos(theta*np.pi/180), r*np.sin(theta*np.pi/180))
    
    def find_line_params(self, x1: float, y1: float, x2: float, y2: float) -> Tuple[float, float]:
        """Find k and b in y=kx+b line equation given two points (x1, y1) and (x2, y2) that belong to that line"""
        dx = x2-x1
        dy = y2-y1
        k = dy/dx
        b = (y1-k*x1)/2+ (y2-k*x2)/2
        self.dataholder.all_lines_params.append((k,b))
        return (k,b)

    def get_more_points_from_params(self, k: float, b: float, central_point: Tuple[float, float], scale: float = 5, point_number: int = 100) -> np.ndarray[Any, np.dtype[np.floating[Any]]]:
        """Generate points on a line y=kx+b defined by params k and b. This function is used to generate points for plt.plot() function"""
        assert np.isclose((central_point[1]-b)/k, central_point[0])
        x_center = central_point[0]
        x_start = x_center - scale
        x_end = x_center + scale
        x_points = np.linspace(x_start, x_end, point_number)
        y_points = k * x_points + b
        return np.dstack((x_points, y_points))
    
    def find_source(self) -> Tuple[float, float]:
        if len(self.dataholder.intersection_points) == 0:
            raise ValueError(f"Can\'t find source, because no intersection points are provided. Intersection points: {self.dataholder.intersection_points}")
        self.dataholder.source = tuple(np.mean(np.array(self.dataholder.intersection_points), axis=0))
        return self.dataholder.source
