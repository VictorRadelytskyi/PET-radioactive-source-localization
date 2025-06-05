from PET_radioactive_source_localization.abstractions.ICalculator import ICalculator
from PET_radioactive_source_localization.implementations.DataHolder import DataHolder
from typing import List, Tuple, Literal, Any, Callable, Dict, Optional, Iterable
import numpy as np
from autograd.numpy import cos, sin #type: ignore
from autograd import grad
from loguru import logger

class LineCalculator(ICalculator):
    def __init__(self, dataholder: DataHolder) -> None:
        self.dataholder = dataholder

    def find_theta_uncertainities(self) -> None:
        try:
            if not self.dataholder.S_thetas:
                logger.warning(f'Statistical error in dataholder is None: {self.dataholder.S_thetas}')
                default_value = (self.dataholder.U_thetas, self.dataholder.U_thetas)
                self.dataholder.u_thetas = [default_value] * len(self.dataholder.thetas)
            else: 
                self.dataholder.u_thetas = [
                        (self.scalar_norm(S_theta1, self.dataholder.U_thetas), 
                        self.scalar_norm(S_theta2, self.dataholder.U_thetas))
                        for S_theta1, S_theta2 in self.dataholder.S_thetas
                    ]
        except AttributeError as e:
            print(f'failed to compute uncertainities of thetas : {e}. Maybe some attribute doesn\'t exist?')

    def find_cartesian_from_polar(self, r: Literal["R1", "R2"], theta: float) -> Tuple[float, float]:
        """get cartesian coordinates of a point, knowing it\'s radius and theta in degrees in polar coordinates"""
        try: 
            r = getattr(self.dataholder, r) 
        except AttributeError as e:
            raise ValueError(f"Radius '{r}' not found in dataholder: {e}")

        return (r*np.cos(theta*np.pi/180), r*np.sin(theta*np.pi/180))
    
    def find_points(self, find_u: bool = False) -> None:
        if not self.dataholder.thetas:
            raise ValueError(f'thetas is None: {self.dataholder.thetas}')
        else: 
            if len(self.dataholder.thetas) == 0:
                raise ValueError(f'thetas is empty: {self.dataholder.thetas}')

        if not self.dataholder.u_thetas:
            raise ValueError(f'u_thetas is None: {self.dataholder.u_thetas}')
        else: 
            if len(self.dataholder.u_thetas) == 0:
                raise ValueError(f'u_thetas is empty: {self.dataholder.u_thetas}')
            
        for theta1, theta2 in self.dataholder.thetas:
            self.dataholder.points.append((self.find_cartesian_from_polar("R1", theta1), self.find_cartesian_from_polar("R2", theta2)))
        
        if not self.dataholder.points:
            raise ValueError(f'points is None: {self.dataholder.points}')
        else: 
            if len(self.dataholder.points) == 0:
                raise ValueError(f'points is empty: {self.dataholder.points}')
            
        if find_u:
            for (theta1, theta2), (u_theta1, u_theta2) in zip(self.dataholder.thetas, self.dataholder.u_thetas):
                u_x1 = self.find_uncertainty_of_composed_function(lambda r, theta: r*cos(theta*np.pi/180), {'r': float(self.dataholder.R1), 'theta': float(theta1)}, {'r': self.dataholder.u_R1, 'theta': u_theta1})
                u_y1 = self.find_uncertainty_of_composed_function(lambda r, theta: r*sin(theta*np.pi/180), {'r': float(self.dataholder.R1), 'theta': float(theta1)}, {'r': self.dataholder.u_R1, 'theta': u_theta1})
                u_x2 = self.find_uncertainty_of_composed_function(lambda r, theta: r*cos(theta*np.pi/180), {'r': float(self.dataholder.R1), 'theta': float(theta2)}, {'r': self.dataholder.u_R2, 'theta': u_theta2})
                u_y2 = self.find_uncertainty_of_composed_function(lambda r, theta: r*sin(theta*np.pi/180), {'r': float(self.dataholder.R1), 'theta': float(theta2)}, {'r': self.dataholder.u_R2, 'theta': u_theta2})

                self.dataholder.u_points.append(((u_x1, u_y1), (u_x2, u_y2)))


    def find_line_params(self, find_u: bool = False) -> None:
        """Find k and b in y=kx+b line equation given two points (x1, y1) and (x2, y2) that belong to that line"""
        if not self.dataholder.points:
            raise ValueError(f'dataholder points is None: {self.dataholder.points}')
        else:
            if len(self.dataholder.points) == 0:
                raise ValueError(f'dataholder points is an empty list: {self.dataholder.points}')
        if not find_u:
            for (x1, y1), (x2, y2) in self.dataholder.points:
                dx = x2-x1
                dy = y2-y1
                k = dy/dx
                b = (y1-k*x1)
                self.dataholder.all_lines_params.append((k,b))
        else:
            if not self.dataholder.u_points:
                raise ValueError(f'dataholder points\'s uncertainties is None: {self.dataholder.u_points}')
            else:
                if len(self.dataholder.points) == 0:
                    raise ValueError(f'dataholder points is an empty list: {self.dataholder.points}')
            for ((x1, y1), (x2, y2)), ((u_x1, u_y1), (u_x2, u_y2)) in zip(self.dataholder.points, self.dataholder.u_points): 
                dx = x2-x1
                dy = y2-y1
                k = dy/dx
                b = (y1-k*x1)/2 + (y2-k*x2)/2
                self.dataholder.all_lines_params.append((k,b))
                u_k = self.find_uncertainty_of_composed_function(lambda x1, y1, x2, y2: (y2-y1)/(x2-x1), {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}, {'x1': u_x1, 'y1': u_y1, 'x2': u_x2, 'y2': u_y2})
                u_b = self.find_uncertainty_of_composed_function(lambda x1, y1, x2, y2: (y1-k*x1)/2 + (y2-k*x2)/2, {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}, {'x1': u_x1, 'y1': u_y1, 'x2': u_x2, 'y2': u_y2})
                #u_b = np.sqrt(u_y1**2+(x1*u_k)**2+(k*u_x1)**2)
                self.dataholder.u_all_lines_params.append((u_k, u_b))

    def get_more_points_from_params(self, k: float, b: float, central_point: Tuple[float, float], scale: float = 5, point_number: int = 100) -> np.ndarray[Any, np.dtype[np.floating[Any]]]:
        """Generate points on a line y=kx+b defined by params k and b. This function is used to generate points for plt.plot() function"""
        assert np.isclose((central_point[1]-b)/k, central_point[0])
        x_center = central_point[0]
        x_start = x_center - scale
        x_end = x_center + scale
        x_points = np.linspace(x_start, x_end, point_number)
        y_points = k * x_points + b
        return np.dstack((x_points, y_points)) 
    
    def find_intersection_point_of_two_lines(self, 
                                             first_line_params: Tuple[float, float], 
                                             second_line_params: Tuple[float, float],
                                             k_epsilon = 0.2, find_u: bool = False, 
                                             u_first_line: Optional[Tuple[float, float]] = None,
                                             u_second_line: Optional[Tuple[float, float]] = None
                                             ) -> Optional[Tuple[float, float] | Tuple[Tuple[float, float], Tuple[float, float]]]:
        """Find intersection of two lines: y1=k1x1+b1 and y2=k2x2+b2. 
        k_epsilon makes sure lines are not too parallel to cause large error
        It's guaranteed to have exactly 1 solution unless k1=k2 meaning the lines are parallel
        """
        k1, b1 = first_line_params
        k2, b2 = second_line_params
        if np.abs(k2-k1) > k_epsilon:
            if not find_u:
                x = (b2-b1)/(k1-k2)
                y = k1*x+b1
                self.dataholder.intersection_points.append((x,y))
                return (x,y)
            else:
                x = (b2-b1)/(k1-k2)
                y = k1*x+b1
                self.dataholder.intersection_points.append((x,y))
                if not u_first_line or not u_second_line:
                    raise ValueError(f'flag find_u to find uncertainties is set to True, meanwhile no uncertainties provided: {u_first_line}, {u_second_line}')
                u_k1, u_b1 = u_first_line
                u_k2, u_b2 = u_second_line
                u_x = self.find_uncertainty_of_composed_function(lambda k1, b1, k2, b2: (b2-b1)/(k1-k2), {"k1": k1, "b1": b1, "k2": k2, "b2": b2}, {"k1": u_k1, "b1": u_b1, "k2": u_k2, "b2": u_b2})
                u_y = self.find_uncertainty_of_composed_function(lambda k1, b1: k1*x+b1, {"k1": k1, "b1": b1}, {"k1": u_k1, "b1": u_b1})
                self.dataholder.u_intersection_points.append((u_x, u_y))
                return ((x, y), (u_x, u_y))
        
    def find_all_intersection_points(self, k_epsilon = 0.2, find_u: bool = False) -> None:
        """Find all the intersection points of multiple lines y1=k1x1+b1,...,y_n=k_n*x_n+b_n. It's guaranteed to have (n-1)! solution unless the list contains parallel lines"""
        if len(self.dataholder.all_lines_params) == 0:
            raise ValueError(f'can\'t find intersection point of all lines, because all_lines_params is empty: {self.dataholder.all_lines_params}')
        
        if not find_u: 
            for i, (k_i, b_i) in enumerate(self.dataholder.all_lines_params[:-1]):
                for (k_j, b_j) in self.dataholder.all_lines_params[i+1:]:
                        self.find_intersection_point_of_two_lines((k_i, b_i), (k_j, b_j), k_epsilon = k_epsilon)
        else:
            if not self.dataholder.u_all_lines_params:
                raise ValueError(f'line params is None: {self.dataholder.u_all_lines_params}')
            else: 
                if len(self.dataholder.u_all_lines_params) == 0:
                    raise ValueError(f'lines params is an empty list: {self.dataholder.u_all_lines_params}')
                
            for i, ((k_i, b_i), (u_k_i, u_b_i)) in enumerate(zip(self.dataholder.all_lines_params[:-1], self.dataholder.u_all_lines_params[:-1])):
                for ((k_j, b_j), (u_k_j, u_b_j)) in zip(self.dataholder.all_lines_params[i+1:], self.dataholder.u_all_lines_params[i+1:]):
                        self.find_intersection_point_of_two_lines((k_i, b_i), (k_j, b_j), k_epsilon = k_epsilon, find_u=True, u_first_line=(u_k_i, u_b_i), u_second_line=(u_k_j, u_b_j))
    
    def find_source(self, find_u: bool = False) -> Tuple[float, float]:
        """Given intersection points, find their mean coordinates, which is the estimated position of the source"""
        if len(self.dataholder.intersection_points) == 0:
            raise ValueError(f"Can\'t find source, because no intersection points are provided. Intersection points: {self.dataholder.intersection_points}")
        self.dataholder.source = tuple(np.mean(np.array(self.dataholder.intersection_points), axis=0))
        if find_u:
            if not self.dataholder.u_intersection_points:
                raise ValueError(f'intersection points uncertainties is None: {self.dataholder.u_intersection_points}')
            else: 
                if len(self.dataholder.u_intersection_points) == 0:
                    raise ValueError(f'intersection points uncertainties is an empty list: {self.dataholder.u_intersection_points}')
            u_x_source = 0
            u_y_source = 0
            n_points = len(self.dataholder.u_intersection_points)
            for u_x, u_y in self.dataholder.u_intersection_points:
                u_x_source += (u_x/n_points)**2
                u_y_source += (u_y/n_points)**2
            self.dataholder.u_source = (np.sqrt(u_x_source), np.sqrt(u_y_source))
        return self.dataholder.source
    
    def find_uncertainty_of_composed_function(
            self,
            f: Callable,
            vars: Dict[str, float],
            u_vars: Dict[str, float]
        ) -> float:
            """
            Computes uncertainty of f(vars) using error propagation.
            Works with keyword-based lambdas like `lambda r, theta: r*np.cos(theta)`.

            Args:
                f: Function (e.g., `lambda r, theta: r*np.cos(theta)`).
                vars: Variable values (e.g., `{'r': 1.0, 'theta': 0.5}`).
                u_vars: Uncertainties (e.g., `{'r': 0.1, 'theta': 0.01}`).

            Returns:
                Propagated uncertainty.
            """
            if vars.keys() != u_vars.keys():
                raise ValueError("Variables and uncertainties must have the same keys")

            # Convert f(r, theta) to f(positional_args) for Autograd
            ordered_vars = list(vars.values())  
            ordered_uncertainties = list(u_vars.values())  

            # Wrapper to convert positional args back to keyword args
            def positional_f(*args):
                kwargs = dict(zip(vars.keys(), args))
                return f(**kwargs)

            sum_sq = 0.0
            for i, (var_name, value) in enumerate(vars.items()):
                # Compute ∂f/∂x_i using the positional wrapper
                df_dxi = grad(positional_f, i)(*ordered_vars)
                sum_sq += (df_dxi * ordered_uncertainties[i]) ** 2

            return np.sqrt(sum_sq)
        
    def round(self, arr: Iterable, n_digits=2) -> Optional[List[Tuple[float, float]] | Tuple[float, float]]:
        try: 
            if isinstance(arr, list):
                return [(round(float(x), n_digits), round(float(y), n_digits)) for x, y in arr]
            elif isinstance(arr, tuple):
                return (round(float(arr[0]), n_digits), round(float(arr[1]), n_digits))
        except Exception as e:
            raise ValueError(f'can\'t round {arr}: {e}')
    
    def scalar_norm(self, *args) -> float:
        return np.sqrt(np.sum([arg**2 for arg in args]))
    
