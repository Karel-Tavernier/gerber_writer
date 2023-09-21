version = '0.3.1'
from src.gerber_writer.writer import (DataLayer, Path, set_generation_software)

def btest(profile):
    profile.moveto((0, 0))
    profile.lineto((100, 0))
    profile.lineto((100, 100))
    profile.lineto((0, 100))
    profile.arcto((0, 0), (50, 50), '+')

set_generation_software('Karel Tavernier', 'gerber_writer_example_outline.py', version)
profile_layer = DataLayer('Profile,NP')
profile = Path()

btest(profile)

# adf
profile_layer.add_region(profile,'Conductor')
profile_layer.add_traces_path(profile, 0.5, 'Profile')
with open('gerbers/ze-bug.gbr', 'w') as outfile:
    profile_layer.dump_gerber(outfile)

