
Readme of gerber_writer
=======================

Purpose
-------

This Python library for generating Gerber files, with the following benefits over writing Gerber files directly from the spec:

* No need to read the 200 page Gerber format specification.
* A much simpler API than the Gerber format specification -8 pages vs 200,
* Built-in pad with all common shapes.
* User-defined pad for special shapes
* 100% compliance with the specification, rev 2022.02.
* Conservative, robust output files. Risky constructions that fail in some buggy implementations are avoided.
* Include meta information need for fabrication, such as what pads are via, in a standardized manner.
* Input methods verify whether the parameters comply with the Gerber spec.
* Stateless input (the gerber_writer takes care of the Gerber states).


Requirements
------------

* Python 3.10 or higher
* Python standard library only
* OS. The library contains no obvious OS dependencies. It has only been tested on Windows 11. Keep me posted if you tested it on others,

License
-------

 Apache 2.0 license
 
 Contact
 -------
 
 karel_tavernier@hotmail.com