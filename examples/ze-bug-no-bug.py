version = '0.3.1'
from src.pius import (DataLayer, Path, set_generation_software)

def atest(profile):
    right = 12000
    up = 200000
    profile.moveto((0, 0))
    profile.lineto((right , 0))
    profile.lineto((right , 100))
    profile.lineto((-right -4000000, up))
    profile.lineto((0, 0))

set_generation_software('ikke', 'gerber_writer_example_outline.py', version)
profile_layer = DataLayer('Profile,NP')
profile = Path()

atest(profile)

profile_layer.add_region(profile,'Conductor')
profile_layer.add_traces_path(profile, 0.5, 'Profile')

# adf
from pathlib import Path
file_out = 'gerbers/' + Path(__file__).stem +'.gbr'
with open(file_out, 'w') as outfile:
    profile_layer.dump_gerber(outfile)
