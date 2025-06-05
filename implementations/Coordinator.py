from PET_radioactive_source_localization.implementations.DataHolder import DataHolder
from PET_radioactive_source_localization.abstractions import *
from typing import List, Tuple, Literal, Optional
import json
import os
import matplotlib.pyplot as plt

class PET:
    def __init__(self, dataholder: DataHolder, calculator: ICalculator, plotter: IPlotter) -> None:
        self.dataholder: DataHolder = dataholder
        self.calculator: ICalculator = calculator
        self.plotter: IPlotter = plotter
    
    def save(self, what: Literal["source", "intersection_points", "both"], 
         output_dir: str, filename_with_ext: str, save_u: bool = True) -> None:
        """Save data to JSON file with optional uncertainties.
        
        Args:
            what: Data to save ("source", "intersection_points", or "both")
            output_dir: Output directory path
            filename_with_ext: Filename with extension (e.g., "data.json")
            save_u: Whether to save uncertainties
        """
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename_with_ext)
        
        # Clear file if it's the first write
        if what == "both" or not os.path.exists(filepath):
            open(filepath, 'w').close()
        
        if what == "both":
            self.save_attr_to_json("source", filepath)
            self.save_attr_to_json("intersection_points", filepath)
            if save_u:
                self.save_attr_to_json("u_source", filepath)
                self.save_attr_to_json("u_intersection_points", filepath)
        else:
            self.save_attr_to_json(what, filepath)
            if save_u:
                self.save_attr_to_json(f"u_{what}", filepath)


    def save_attr_to_json(self, attr_name: str, filepath: str, round: bool = True) -> None:
        """Internal method to save a single attribute to JSON file."""
        if not hasattr(self.dataholder, attr_name):
            raise AttributeError(f"DataHolder has no attribute '{attr_name}'")
        
        attr_value = getattr(self.dataholder, attr_name)
        if attr_value is None:
            raise ValueError(f"Cannot save None value for attribute '{attr_name}'")
        
        if round:
            attr_value = self.calculator.round(attr_value) #type: ignore
        
        existing_data = {}
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            with open(filepath, 'r') as f:
                existing_data = json.load(f)
        
        existing_data[attr_name] = attr_value
        
        with open(filepath, 'w') as f:
            json.dump(existing_data, f, indent=2)
                
            
    def run(self, filename: str, output_dir: str = r"processed_data", scale: float = 5, k_epsilon: float = 0.2, save_plot: bool = True, save_source: bool = True, save_intersection_points: bool = True) -> Optional[Tuple[float, float]]: 
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", output_dir))
        if not os.path.isdir(output_dir):
            raise FileNotFoundError(f'output directory: {output_dir} is not a valid directory')
        
        if len(self.dataholder.thetas) == 0 or self.dataholder is None:
            raise ValueError(f'can\'t find thetas in dataholder: {self.dataholder.thetas}')
        if len(self.dataholder.thetas) == 0:
            raise ValueError(f'No thetas provided: {self.dataholder.thetas}')
        
        
        self.calculator.find_theta_uncertainities()
        print(f'u_thetas: {self.dataholder.u_thetas}')
        self.calculator.find_points(find_u=True)
        print(f'\n\nprinting points: {self.dataholder.points} \n\n')
        print(f'\n\nprinting points\'s uncertainties: {self.dataholder.u_points} \n\n')
        self.calculator.find_line_params(find_u=True)
        print(f'\n\nprinting params: {self.dataholder.all_lines_params} \n\n')
        print(f'\n\nprinting params\'s uncertainties: {self.dataholder.u_all_lines_params} \n\n')
        self.calculator.find_all_intersection_points(k_epsilon=k_epsilon, find_u=True)
        print(f'\n\nprinting intersection points: {self.dataholder.intersection_points} \n\n')
        print(f'\n\nprinting intersection points\'s uncertainties: {self.dataholder.u_intersection_points} \n\n')
        self.calculator.find_source(find_u=True)
        print(f'\n\nprinting source: {self.dataholder.source} \n\n')
        print(f'\n\nprinting source uncertainty: {self.dataholder.u_source} \n\n')
        
        x_arr, y_arr = ([], [])
        for (k, b), ((x1, y1), (x2, y2)) in zip(self.dataholder.all_lines_params, self.dataholder.points):
            points = self.calculator.get_more_points_from_params(k, b, central_point=(x1/2+x2/2, y1/2+y2/2), scale = scale)[0]
            x_arr = points[:, 0]
            y_arr = points[:, 1]
            self.plotter.add_points(x_arr, y_arr)
        self.plotter.highlight_intersection_points(show_uncertainties=True)
        self.plotter.highlight_source(show_uncertainty=True)

        if save_plot:
            filepath = os.path.join(output_dir, "images", filename+".png")
            if not os.path.exists(os.path.dirname(filepath)):
                raise FileNotFoundError(f'directory of filepath: {filepath} does not exist')
            plt.savefig(filepath)
            self.plotter.finalize(save = True, filepath=filepath) #type: ignore
        else: 
            self.plotter.finalize() #type: ignore

        if save_source and save_intersection_points:
            self.save("both", output_dir=output_dir, filename_with_ext=filename+".json")
        else:
            if save_source:
                self.save("source", output_dir=output_dir, filename_with_ext=filename+".json")
            if save_intersection_points:
                self.save("intersection_points", output_dir=output_dir, filename_with_ext=filename+".json")

