Readme of gerber_writer
=======================

Purpose
-------

A Python library for writing Gerber files. 

Its benefits over writing Gerber files directly from the spec are:

* No need to read the 200 page Gerber format specification.
* A much simpler API than the Gerber format specification -8 pages vs 200,
* Built-in pad with all common shapes.
* User-defined pad for special shapes
* 100% compliance with the specification, rev 2022.02.
* Conservative, robust output files. Risky constructions that fail in some buggy implementations are avoided.
* Include meta information need for fabrication, such as what pads are via, in a standardized manner.
* Input methods verify whether the parameters comply with the Gerber spec.
* Stateless input (the gerber_writer takes care of the Gerber states).

Example:: 

	from gerber_writer import DataLayer, Path    
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
	with open('gerbers\profile.gbr', 'w') as outfile:
		profile_layer.dump_gerber(outfile)

Installation
------------

py -m pip install gerber_writer

Requirements
------------

* Python 3.10 or higher
* Standard library only.
* OS independent. Only tested on Windows 11. Let me know if you tested it on other OSs.

License
-------

Apache 2.0 license
 
Contact
-------
 
karel_tavernier@hotmail.com