from PET_radioactive_source_localization.implementations import *
import PET_radioactive_source_localization.lab_data.single_source as lab_data
from typing import List, Tuple

def run(thetas: List[Tuple[float, float]], filename: str, output_dir: str = r"processed_data", scale: float = 5, saveplot: bool = True, savesource: bool = True, mode: str = 'w'):
    dataholder = DataHolder()
    plotter = Plotter(dataholder=dataholder)
    calculator = LineCalculator(dataholder=dataholder)
    pet = PET(dataholder, calculator, plotter)

    pet.run(thetas, filename, output_dir=output_dir, scale = scale, saveplot=saveplot, savesource=savesource, mode=mode)

if __name__ == "__main__":
    run(lab_data.thetas, "single_source")

