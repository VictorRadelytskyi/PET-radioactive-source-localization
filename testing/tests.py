import pytest
from PET_radioactive_source_localization.implementations.LineCalculator import LineCalculator
from PET_radioactive_source_localization.implementations.DataHolder import DataHolder

from math import isclose
import numpy as np

def test_get_line_params():
    dataholder = DataHolder()
    calculator = LineCalculator(dataholder)
    k, b = calculator.find_line_params(1, 1, 2, 2)

    assert isclose(k, 1)
    assert isclose(b, 0)

def test_get_more_points_from_params():
    dataholder = DataHolder()
    calculator = LineCalculator(dataholder)
    points = calculator.get_more_points_from_params(k=1, b=0, central_point=(0.0, 0.0), scale=5, point_number = 11)[0]
    print(points)
    expected = [[-5, -5], [-4, -4], [-3, -3], [-2, -2], [-1, -1], [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]

    assert np.allclose(points, expected)

def test_find_intersection_point_of_two_lines():
    dataholder = DataHolder()
    calculator = LineCalculator(dataholder)
    result = calculator.find_intersection_point_of_two_lines((1,0), (-1, 2))
    x = 0
    y = 0
    if result: 
        x, y = result
    assert np.allclose((x,y), (1, 1))

def test_all_intersection_points():
    dataholder = DataHolder()
    calculator = LineCalculator(dataholder)
    calculator.dataholder.all_lines_params = [(0,1), (-2, 2), (2,-2)]
    calculator.find_all_intersection_points()
    assert np.allclose(calculator.dataholder.intersection_points, [(0.5, 1), (1.5, 1), (1, 0)])