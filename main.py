from PET_radioactive_source_localization.implementations import *
import PET_radioactive_source_localization.lab_data.single_source as single_source
import PET_radioactive_source_localization.lab_data.double_source_1 as double_source_1
import PET_radioactive_source_localization.lab_data.double_source_2 as double_source_2
from typing import List, Tuple, Optional

def run(thetas: List[Tuple[float, float]], filename: str, S_thetas: Optional[List[Tuple[float, float]]] = None, output_dir: str = r"processed_data", scale: float = 5, k_epsilon: float = 0.2, save_plot: bool = True, save_source: bool = True, save_intersection_points: bool = True) -> None:
    dataholder = DataHolder(thetas=thetas)
    if S_thetas: 
        dataholder = DataHolder(thetas=thetas, S_thetas=S_thetas)
    plotter = Plotter(dataholder=dataholder)
    calculator = LineCalculator(dataholder=dataholder)
    pet = PET(dataholder, calculator, plotter)

    pet.run(filename, output_dir=output_dir, scale = scale, k_epsilon=k_epsilon, save_plot=save_plot, save_source=save_source, save_intersection_points = save_intersection_points)

if __name__ == "__main__":
    #run(single_source.thetas, "single_source", S_thetas = single_source.S_thetas, save_plot = True, save_source = True, save_intersection_points = True)
    #run(double_source_1.thetas_weaker, "double_source_1_Weaker", S_thetas = double_source_1.S_thetas_weaker, save_plot = True, save_source = True, save_intersection_points = True)
    #run(double_source_1.thetas_stronger, "double_source_1_Stronger", S_thetas = double_source_1.S_thetas_stronger, save_plot = True, save_source = True, save_intersection_points = True)
    #run(double_source_2.thetas_weaker, "double_source_2_Weaker", S_thetas = double_source_2.S_thetas_weaker, k_epsilon=0.4, save_plot = True, save_source = True, save_intersection_points = True)
    #run(double_source_2.thetas_stronger, "double_source_2_Stronger", S_thetas = double_source_2.S_thetas_stronger, save_plot = True, save_source = True, save_intersection_points = True)
