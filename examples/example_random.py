""" Generate Gerber file with random flashes and random walk."""
# KT, 07-May-2022
version = '0.3.1'

from math import sqrt
from random import uniform
from time import time

from gerber_writer import (DataLayer, Circle)
# from src.gerber_writer.writer import (DataLayer, Circle)


RANGE = 1_000
ITERATIONS = 1000

def random_point(): return (uniform(-RANGE, RANGE), uniform(-RANGE, RANGE))

layer = DataLayer('Other,random_test')
start = time()
print(f"{ITERATIONS} iterations")
# random circle pads
for _ in range(ITERATIONS):
    layer.add_pad(Circle(0.015, ''), random_point())
end_add_pad = time()
print(f'Add pads (s): {end_add_pad - start}')
# random walk
step = RANGE/sqrt(ITERATIONS)
start_point = (0, 0)
for _ in range(ITERATIONS):
    next_point = (start_point[0] + uniform(-step, step),
                  start_point[1] + uniform(-step, step))
    layer.add_trace_line(start_point, next_point, 0.01, '')
    start_point = next_point
end_add_traces = time()
print(f'Add lines (s): {end_add_traces - end_add_pad}')
with open('gerbers/gerber_writer_random.gbr', 'w') as outfile:
    layer.dump_gerber(outfile)
end_dump = time()
print('Dump to file (s):', end_dump - end_add_traces)
