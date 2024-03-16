Readme
======

Purpose
-------

A Python library for writing Gerber files.

* No need to read the 200 page Gerber format specification.
* API much simpler than the Gerber format specification - 8 pages vs 200.
* All common pad shapes built-in.
* User-defined pad special shapes
* 100% compliance with the specification, rev 2022.02.
* Conservative, robust output files.
* Risky constructs that fail in some buggy implementations are not used.
* Include standardized meta information needed for fabrication, such as which pads are vias.
* Verify whether the input parameters comply with the Gerber spec.
* Stateless input (the gerber_writer takes care of the Gerber states).

Example:

.. code-block:: python

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

.. image:: https://github.com/Karel-Tavernier/gerber_writer/assets/56170852/7b351186-9cdc-4cc0-9f3b-04708ee50216
	:width: 800

Installation
------------

This package requires Python 3.9 or later, you can find it `here <https://www.python.org/downloads/>`_.

+++++++
Windows
+++++++

.. code-block:: batch

	$ py -m pip install gerber_writer

+++++
Linux
+++++

.. code-block:: batch

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