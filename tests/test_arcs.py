# KT, 2022 08 05

version = '0.3.4'

import hashlib
# import os
import pytest

from src.gerber_writer.writer import _pnt_orientation
# from writer import _pnt_orientation
from src.gerber_writer import DataLayer


def body_md5(layer):
    """Return the md5 string of the layer gerber string, excluding datetime and version statements"""
    tested_gerber_section = (layer.dumps_gerber().partition('.CreationDate')[2])[30:]
    return (hashlib.md5(tested_gerber_section.encode())).hexdigest()


output_gerbers = True  # Useful during debugging to have the gerbers for inspection
folder = '/home/alaindef/projects/pycharm-projects-py3/gerber_writer/tools/gerbers/'  # Root directory for gerbers


# folder = '../examples/gerbers/' # Root directory for gerbers
# folder = '../tools/gerbers/' # Root directory for gerbers


# adf 230920 playing with tutorial things.
@pytest.mark.parametrize("num, output", [((1, -1), '-'), ((1, 0), '0'), ((1, 1), '+')])
def test_orientation_multiple(num, output):
    assert _pnt_orientation((0, 0), (1, 0), num) == output


def test_orientation():
    assert _pnt_orientation((0, 0), (1, 0), (1, -1)) == '-'
    assert _pnt_orientation((0, 0), (1, 0), (1, 0)) == '0'
    # assert _pnt_orientation((0, 0), (1, 0), (1, +1)) == 'qq'
    assert _pnt_orientation((0, 0), (1, 0), (1, +1)) == '+'


# adf
@pytest.mark.skip
def test_short_chords():
    test_layer = DataLayer('Other,Test short chord')
    test_layer.add_trace_arc((-2, 2), (-1.5, 1.5), (-1.5, 2), '+', 0.04, 'Conductor')
    short = 0.0001
    test_layer.add_trace_arc((-1.5, 1.5), (-1.5 + 2 * short, 1.5), (-1.5 + short, 1.5 + 10), '-', 0.04, 'Conductor')
    test_layer.add_trace_arc((-1, 1.5), (-1 + 2 * short, 1.5), (-1 + short, 1.5 + 10), '+', 0.04, 'Conductor')
    test_layer.add_trace_arc((0, 1.5), (0 + 2 * short, 1.5), (0 + short, 1.5 + 3 * short), '+', 0.04, 'Conductor')
    if output_gerbers:
        with open(folder + 'pytest_arc.gbr', 'w') as outfile:
            # with open(folder + 'pytest_arc.gbr', 'w') as outfile:
            test_layer.dump_gerber(outfile)
    assert body_md5(test_layer) == '538b42907bf992772344c83d43b316d5'


def test_invalid_arcs():
    test_layer = DataLayer('Other,Test invalid arc')
    with pytest.raises(ValueError):
        test_layer.add_trace_arc((0, 0), (1, 0), (0.4999, 1), '+', 0.1, 'Conductor')
