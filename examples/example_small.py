"""gerber_writer small sample file"""
# Copyright: Karel Tavernier
# Creation date: 18-August-2022

# adf: if you use "from gerber_writer ..." you use the package, which has to be installed with pip
# when the local python3 of the venv is configured, the package must also be installed in venv
# when the package is NOT installed, the second form has to be used: "from src.gerber_writer.writer import..."
from gerber_writer import DataLayer, Circle, RoundedRectangle
# from src.gerber_writer.writer import DataLayer, Circle, RoundedRectangle
# (when running without pip installed package)

trace_width = 0.508
via_pad = Circle(0.508, 'ViaPad')
IC17_toe = RoundedRectangle(1.257, 2.286, 0.254, 'SMDPad,CuDef')
toe_point = (0, 2.54)
# via_point = (5000, 0)
via_point = (5.08, 0)

top = DataLayer('Copper,L1,Top,Signal')

top.add_pad(IC17_toe, toe_point, angle=45)
top.add_trace_line(toe_point, (2.54, 0), trace_width, 'Conductor')
top.add_trace_line((2.54, 0), via_point, trace_width, 'Conductor')
top.add_pad(via_pad, via_point)

with open('gerbers/gerber_writer_example_small.gbr', 'w') as outfile:
    top.dump_gerber(outfile)
