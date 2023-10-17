# Example file for gerber_writer
# Generates a PCB profile
# KT, 22-May-2022
version = '0.3.1'

from gerber_writer import (DataLayer, Path, set_generation_software)
    
set_generation_software('Karel Tavernier', 'gerber_writer_example_outline.py', version)    
profile_layer = DataLayer('Profile,NP')    
profile = Path()
profile.moveto((0, 0))
profile.lineto((150, 0))
profile.arcto((160, 10), (160, 0), '-')
profile.lineto((170, 10))
profile.lineto((170, 90))
profile.lineto((160, 90))
profile.arcto((150, 100), (160, 100), '-')
profile.lineto((0, 100))
profile.lineto((0, 0))
profile_layer.add_traces_path(profile, 0.5, 'Profile')
with open('gerbers/gerber_writer_example_outline.gbr', 'w') as outfile:
    profile_layer.dump_gerber(outfile)
