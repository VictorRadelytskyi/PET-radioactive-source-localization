from PET_radioactive_source_localization.implementations.DataHolder import DataHolder
from PET_radioactive_source_localization.abstractions import *
from typing import Tuple, List, Optional
import os
import sys
import matplotlib.pyplot as plt

class PET:
    def __init__(self, dataholder: DataHolder, calculator: ICalculator, plotter: IPlotter) -> None:
        self.dataholder: DataHolder = dataholder
        self.calculator: ICalculator = calculator
        self.plotter: IPlotter = plotter
    
    def run(self, thetas: List[Tuple[float, float]], filename: str, output_dir: str = r"processed_data", scale: float = 5, saveplot: bool = True, savesource: bool = True, mode: str = 'w') -> Optional[Tuple[float, float]]: 
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", output_dir))
        if not os.path.isdir(output_dir):
            raise FileNotFoundError(f'output directory: {output_dir} is not a valid directory')
        if len(thetas) == 0:
            raise ValueError(f'No thetas provided: {thetas}')
        
        x_arr, y_arr = ([], [])
        for theta1, theta2 in thetas:
            try:
                x1, y1 = self.calculator.find_cartesian_from_polar("R1", theta1)
                x2, y2 = self.calculator.find_cartesian_from_polar("R2", theta2)
                k, b = self.calculator.find_line_params(*(x1,y1), *(x2,y2))
                points = self.calculator.get_more_points_from_params(k, b, central_point=(x1/2+x2/2, y1/2+y2/2), scale = scale)[0]
                x_arr = points[:, 0]
                y_arr = points[:, 1]
            except Exception as e: 
                raise Exception(f'failed to generate data points for plotter in the run method: {e}')
            self.plotter.add_points(x_arr, y_arr)
        
        self.calculator.find_all_intersection_points()
        self.plotter.highlight_intersection_points()
        self.calculator.find_source()
        self.plotter.highlight_source()

        if savesource:
            filepath = os.path.join(output_dir, filename+".txt")
            if not os.path.exists(os.path.dirname(filepath)):
                raise FileNotFoundError(f'directory of filepath: {filepath} does not exist')
            with open(filepath, mode=mode) as output_file:
                if self.dataholder.source:
                    output_file.write(str(self.dataholder.source))
                else:
                    raise ValueError(f'can\'t write to the output file because the source is None')
                
        if saveplot:
            filepath = os.path.join(output_dir, "images", filename+".png")
            if not os.path.exists(os.path.dirname(filepath)):
                raise FileNotFoundError(f'directory of filepath: {filepath} does not exist')
            plt.savefig(filepath)

        return self.dataholder.source or None
