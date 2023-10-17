# KT, 2022 08 12
# Test whether contour is closed

version = '0.3.4'

import pytest
from src.gerber_writer import DataLayer, Path


def test_contour_validity():
    origin = (0, 0)
    p1 = (1.5, 0)
    p2 = (0, 1.5)

    test_path = Path()
    assert test_path.contour == False
    assert test_path.start_point is None

    test_path.moveto(origin)
    assert test_path.contour == False
    assert test_path.start_point == origin

    test_path.lineto(p1)
    assert test_path.contour == False
    assert test_path.start_point == origin

    test_path.arcto(p2, origin, '+')
    assert test_path.contour == False
    assert test_path.start_point == origin
    assert test_path.current_point == p2

    test_path.lineto(origin)
    assert test_path.contour == True

    test_layer = DataLayer('Other,Test contour validity')
    test_layer.add_traces_path(test_path, 0.1, 'Other,test')

    test_path.moveto(p1)
    assert test_path.contour == False
    with pytest.raises(ValueError):
        test_layer.add_region(test_path, 'Other,test', negative=True)


def test_moveto_presence():
    test_path = Path()
    with pytest.raises(ValueError):
        test_path.lineto((12, 13))
    with pytest.raises(ValueError):
        test_path.arcto((14, 13), (13, 13), '-')
