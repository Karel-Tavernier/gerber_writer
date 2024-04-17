Readme
======

Purpose
-------

A Python library for writing Gerber files. 

* The API is much simpler than the Gerber format specification - 8 pages vs 200.
* No need to read the 200 page Gerber format specification.
* All common pad shapes are built-in.
* User-defined pads shapes are easily created.
* 100% compliance with revision 2023.08 of the Gerber Layer Format Specification.
* Conservative, robust output files.
* Risky constructs failing in some buggy applications are avoided.
* Standardized meta information for fabrication, such as which pads are vias.
* Input parameters are checked for compliance with the Gerber spec.
* Stateless input (the gerber_writer takes care of the Gerber states).

Example:: 

	from gerber_writer import DataLayer, Circle, RoundedRectangle
		
	trace_width = 0.127
	via_pad = Circle(0.508, 'ViaPad')
	IC17_toe = RoundedRectangle(1.257, 2.286, 0.254, 'SMDPad,CuDef')
	toe_point = (0, 2.54)
	via_point = (5.08, 0)

	top = DataLayer('Copper,L1,Top,Signal')

	top.add_pad(IC17_toe, toe_point, angle=45)
	top.add_trace_line(toe_point, (2.54, 0), trace_width, 'Conductor')
	top.add_trace_line((2.54, 0), via_point, trace_width, 'Conductor')
	top.add_pad(via_pad, via_point)

	with open('gerbers\gerber_writer_example_small.gbr', 'w') as outfile:
        top.dump_gerber(outfile)
		
.. image:: https://karel-tavernier.github.io/gerber_writer/html/_images/example_small.png
	:width: 800

Installation
------------

Windows::

    $ py -m pip install gerber_writer
	
Linux::

    $ python3 -m pip install gerber_writer

Requirements
------------

* Python 3.9 or higher
* Standard library only.
* OS independent.

License
-------

Apache 2.0 license
 
Contact
-------
 
karel_tavernier@hotmail.com
