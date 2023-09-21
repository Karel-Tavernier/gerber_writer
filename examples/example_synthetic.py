"""Sample gerber_writer file"""
# Copyright Karel Tavernier

version = '0.1.4'  # gerber_writer version written in Gerber file

from gerber_writer import DataLayer
from gerber_writer import (
    Path, set_generation_software,
    Circle, Rectangle, RoundedRectangle, RoundedThermal
    )
    
trace_width = 0.254
via_pad = Circle(0.508, 'ViaPad')

set_generation_software('Karel Tavernier', 'gerber_writer_example.py', version)
top = DataLayer('Copper,L1,Top,Signal', negative=False)

# Footprint of IC17
IC17_toe = Rectangle(1.27, 2.54, 'SMDPad,CuDef')
top.add_pad(IC17_toe, (65.094, 47.269), 45)
top.add_pad(IC17_toe, (68.047, 50.267), 45)
# Connect one pin to via
top.add_trace_line((65.094, 47.269), (65.094+1, 47.269+1), trace_width, 'Conductor')
top.add_pad(via_pad, (65.094+1, 47.269+1))

# Footprint of IC13
IC16_toe = RoundedRectangle(1.257, 2.286, 0.254, 'SMDPad,CuDef')
t1 = (56.515, 47.879)
t2 = (60.341, 47.879)
t3 = (58.428, 43.700)
footprint = (t1, t2, t3)
for toe_location in footprint:
    top.add_pad(IC16_toe, toe_location)
# Connect pin 2 to via
top.add_trace_line(t2, (62.549, 47.879), trace_width, 'Conductor')
top.add_trace_line((62.549, 47.879), (64.350, 49.657), trace_width, 'Conductor')
top.add_pad(via_pad, (64.350, 49.657))
# Connect pin 3 to IC17
p1 = (65.000, 43.700)
p2 = (65.000+4.8, 43.700+4.8)
p3 = (68.047, 50.267)
con_3_IC17 = Path()
con_3_IC17.moveto(t3)
con_3_IC17.lineto(p1)
con_3_IC17.lineto(p2)
con_3_IC17.lineto(p3)
top.add_traces_path(con_3_IC17, trace_width, 'Conductor')

# Copper pour, rectangle with one rounded corner
x_lft = 55
x_rgt = 63
y_bot = 50
y_top = 56
radius = 2.2
pour = Path()
pour.moveto((x_lft, y_bot))
pour.lineto((x_rgt - radius, y_bot))
pour.arcto((x_rgt, y_bot + radius), (x_rgt - radius, y_bot + radius), '+')
pour.lineto((x_rgt, y_top))
pour.lineto((x_lft, y_top))
pour.lineto((x_lft, y_bot))
top.add_region(pour, 'Conductor')
# Thermal relief pad in copper pour
top.add_pad(RoundedThermal(1, 0.8, 0.06, 'ThermalReliefPad', negative=True),
            (x_rgt - radius, y_bot + radius), angle=45)
# Embedded  via pad in copper pour
top.add_pad(via_pad, (x_lft + radius, y_top - radius))
# Connect pin 1 of IC16 to copper pour
top.add_trace_line(t1, (56.515, 47.879+2.54), trace_width, 'Conductor')

# Connect vias, with arcs, parallel
trace_start = (64, 53)
top.add_pad(via_pad, trace_start)
connection_a = Path()
connection_a.moveto(trace_start)
connection_a.lineto((trace_start[0], trace_start[1]+1))
connection_a.arcto((trace_start[0]+2, trace_start[1]+3), (trace_start[0]+2, trace_start[1]+1), '-')
connection_a.arcto((trace_start[0]+3, trace_start[1]+4), (trace_start[0]+2, trace_start[1]+4), '+')
connection_a.lineto((trace_start[0]+3, trace_start[1]+6))
top.add_traces_path(connection_a, trace_width, 'Conductor', negative=False)
top.add_pad(via_pad, (trace_start[0]+3, trace_start[1]+6), 0)
trace_start = (65, 53)
top.add_pad(via_pad, trace_start)
connection_b = Path()
connection_b.moveto(trace_start)
connection_b.lineto((trace_start[0], trace_start[1]+1))
connection_b.arcto((trace_start[0]+1, trace_start[1]+2), (trace_start[0]+1, trace_start[1]+1), '-')
connection_b.arcto((trace_start[0]+3, trace_start[1]+4), (trace_start[0]+1, trace_start[1]+4), '+')
connection_b.lineto((trace_start[0]+3, trace_start[1]+6))
top.add_traces_path(connection_b, trace_width, 'Conductor')
top.add_pad(via_pad, (trace_start[0]+3, trace_start[1]+6), 0)
with open('gerbers/gerber_writer_example_synthetic.gbr', 'w') as outfile:
    top.dump_gerber(outfile)


