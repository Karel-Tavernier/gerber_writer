===========================
Change log of gerber_writer
===========================

Version 0.4.2.20
----------------

- minimum required python version is now 3.9 instead of 3.10. Too many users are on 3.9  

Version 0.4.2.17
----------------

- paths with '\' changed to '/' when used for both linux and windows,
    a string like "..\abc\def" becomes r"../abc/def". Windows will then back off

Version 0.4.2.15
----------------

- sphinx documentation process updated for linux
- tools directory not under git control anymore, as it is considered private and for developer use

Version 0.4.2.11
----------------

- bug solved: integerdigits returns 2 for pointMax= 500, 3 for pointMax=5000

Version 0.4.2.7
---------------

- bug solved: when pointMax remains zero (because of empty files, no path instructions etc).
    there will be a crash because math.log(pointMax[0]) fails.
    pointMax is now initialised with (1,1)

Version 0.4.1.3
---------------

- corrected 'no error when path ends with arc and is not closed'. added lutils.py for little utilities. added some pytest functionality.
- issue 'max coordinates' solved.
- for linux: PyPI-make-and-upload.sh allows upload to PyPI 


Version 0.4.1.2
--------------- 

- Correct link to image in README.rst

Version 0.4.1
-------------

- Protect against the instability of very small arcs
- Raise exception on invalid arcs (radii to start and end point are too unequal)
- Raise exception when adding contours that are not closed

Version 0.3.4
-------------

Initial release
