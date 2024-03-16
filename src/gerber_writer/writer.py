"""

.. module:: gerber_writer
   :synopsis: A simple API for writing Gerber files
.. moduleauthor:: Karel Tavernier <karel_tavernier@hotmail.com>

Gerber format - a primer
========================

A Gerber file represents the image of PCB layer. 
The image is defined by an ordered list of *graphics objects*. 
*File attributes* identify the purpose of the file, e.g. it is the top copper layer.
*Object attributes* identify the purpose of objects, e.g. that a pad is a via pad of component pad.


Graphics objects
----------------

There are three types of graphics objects:

* Pads
    Pads are geometrics shapes replicated over the board, such as circles for via pads or rounded rectangles for SMD pads. 

* Traces    
    These are either straight line or circular arc segments. They are typically used for traces
    in a copper plane, but are also used to plot text, etc.
    
* Regions
    Regions are defined by their contours. They are typically used for copper pours,
    but they can also be used for a logo, etc.
    
Polarity
--------

The file can have positive or negative polarity.  
In positive files image means presence of material, in negative files its absence.
Solder mask layers are conventionally negative, and it is strongly recommended to stick to that convention.
All other layers are best positive. 
Negative is also sometimes used for copper planes, but there is today no reason for it. It is just confusing.
(Historically, with a technology no longer used since 50 years, there was a reason to do this. No longer. Move with the times.)

Graphics objects can have either positive or negative polarity. Positive is the normal polarity. 
Positive graphics objects are add to the image. Negative ones *erase* the image created by all *preceding* graphics objects.
Thus, in the presence of negative objects, the order of the graphics object list is important.

Function
--------

File function attributes identify the content or function of the file, e.g. 'SolderMask,Top'
Valid file function attribute values are listed as .FileFunction values in the Gerber format specification.
Without function the file is meaningless.
 
Object function attributes identify the function of the object, e.g. 'ViaPad', 'Conductor'. 
Valid object values are listed as .AperFunction  values in the Gerber format specification.
This meta-information is essential for bare-board fabrication. 

Specification
-------------

The Gerber layer format specification_ is available from the official Gerber format website_.

.. _specification: https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2022-02_en.pdf
.. _website: https://www.ucamco.com/en/gerber

Usage
=====

DataLayer is the main class. First all graphics objects and attributes are added to the DataLayer, using the add methods provided.
When the DataLayer is complete the dumps_gerber or dump_gerber methods return the Gerber string or output it as a Gerber file.
On a layer there are typically many identical pads. 
To handle this efficiently one creates a padmaster instance, with a shape and function for instance to define a via pad. 
A range of built-in master pad classes provide for the typical pad shapes such as circle or rectangle with rounded corners,
as well as a class to create pad masters with a user defined shape.
The add_pad method replicates the padmaster at a given position and under a given angle.

A point is consistently represented by a tuple of two floats.

Files can be verified with the Reference_Gerber_Viewer_ on the offical Gerber format website.

.. _Reference_Gerber_Viewer:  https://gerber-viewer.ucamco.com

Overview
========

General Classes
---------------

* **DataLayer**         - The main class, accumulate the graphics objects and output Gerbers.
* **Path**              - Define traces and regions.

Pad Master Classes
------------------

* **Circle**            - Pad master, circular
* **Rectangle**         - Pad master, rectangular
* **RoundedRectangle**  - Pad master, rectangle with rounded corners
* **ChamferedRectangle** - Pad master, rectangle with chamfered corners
* **RegularPolygon**    - Pad master, regular polython
* **Thermal**           - Pad master, a circular thermal with straight corners
* **RoundedThermal**    - Pad master, a circular thermal with rouned corners
* **UserPolygon**       - Pad master, a user defined shape

Methods
-------
* **set_generation_software** - Identify the software that generated the Gerber file

Exceptions
----------

TypeError and ValueError exceptions are thrown on invalid inputs.

Examples
========

Synthetic
---------

>>> from gerber_writer import DataLayer
>>> from gerber_writer import (
...     Path, set_generation_software,
...     Circle, Rectangle, RoundedRectangle, RoundedThermal
...     )
>>>
>>> set_generation_software('Karel Tavernier', 'gerber_writer_example.py', '2022.06')
>>> trace_width = 0.254
>>> via_pad = Circle(0.508, 'ViaPad')
>>> top = DataLayer('Copper,L1,Top,Signal', negative=False)
>>>
>>> # Footprint of IC17
>>> IC17_toe = Rectangle(1.27, 2.54, 'SMDPad,CuDef')
>>> top.add_pad(IC17_toe, (65.094, 47.269), 45)
>>> top.add_pad(IC17_toe, (68.047, 50.267), 45)
>>> # Connect one pin to via
>>> top.add_trace_line((65.094, 47.269), (65.094+1, 47.269+1), trace_width, 'Conductor')
>>> top.add_pad(via_pad, (65.094+1, 47.269+1))
>>>
>>> # Footprint of IC16
>>> IC16_toe = RoundedRectangle(1.257, 2.286, 0.254, 'SMDPad,CuDef')
>>> footprint = ((56.515, 47.879), (60.341, 47.879), (58.428, 43.700))
>>> for toe_location in footprint:
...     top.add_pad(IC16_toe, toe_location)
>>> # Connect pin 2 to via
>>> top.add_trace_line(footprint[1], (62.549, 47.879), trace_width, 'Conductor')
>>> top.add_trace_line((62.549, 47.879), (64.350, 49.657), trace_width, 'Conductor')
>>> top.add_pad(via_pad, (64.350, 49.657))
>>> # Connect pin 3 to IC17
>>> p1 = (65.000, 43.700)
>>> p2 = (65.000+4.8, 43.700+4.8)
>>> p3 = (68.047, 50.267)
>>> con_3_IC17 = Path()
>>> con_3_IC17.moveto(footprint[2])
>>> con_3_IC17.lineto(p1)
>>> con_3_IC17.lineto(p2)
>>> con_3_IC17.lineto(p3)
>>> top.add_traces_path(con_3_IC17, trace_width, 'Conductor')
>>>
>>> # Copper pour, rectangle with one rounded corner
>>> x_lft = 55
>>> x_rgt = 63
>>> y_bot = 50
>>> y_top = 56
>>> radius = 2.2
>>> pour = Path()
>>> pour.moveto((x_lft, y_bot))
>>> pour.lineto((x_rgt - radius, y_bot))
>>> pour.arcto((x_rgt, y_bot + radius), (x_rgt - radius, y_bot + radius), '+')
>>> pour.lineto((x_rgt, y_top))
>>> pour.lineto((x_lft, y_top))
>>> pour.lineto((x_lft, y_bot))
>>> top.add_region(pour, 'Conductor')
>>> # Thermal relief pad in copper pour
>>> top.add_pad(RoundedThermal(1, 0.8, 0.06, 'ThermalReliefPad', negative=True),
...             (x_rgt - radius, y_bot + radius), angle=45)
>>> # Embedded  via pad in copper pour
>>> top.add_pad(via_pad, (x_lft + radius, y_top - radius))
>>> # Connect pin one of IC16 to copper pour
>>> top.add_trace_line(footprint[0], (56.515, 47.879+2.54), trace_width, 'Conductor')
>>> 
>>> # Connect vias, with arcs, parallel
>>> trace_start = (64, 53)
>>> top.add_pad(via_pad, trace_start)
>>> connection_a = Path()
>>> connection_a.moveto(trace_start)
>>> connection_a.lineto((trace_start[0], trace_start[1]+1))
>>> connection_a.arcto((trace_start[0]+2, trace_start[1]+3), (trace_start[0]+2, trace_start[1]+1), '-')
>>> connection_a.arcto((trace_start[0]+3, trace_start[1]+4), (trace_start[0]+2, trace_start[1]+4), '+')
>>> connection_a.lineto((trace_start[0]+3, trace_start[1]+6))
>>> top.add_traces_path(connection_a, trace_width, 'Conductor', negative=False)
>>> top.add_pad(via_pad, (trace_start[0]+3, trace_start[1]+6), 0)
>>> trace_start = (65, 53)
>>> top.add_pad(via_pad, trace_start)
>>> connection_b = Path()
>>> connection_b.moveto(trace_start)
>>> connection_b.lineto((trace_start[0], trace_start[1]+1))
>>> connection_b.arcto((trace_start[0]+1, trace_start[1]+2), (trace_start[0]+1, trace_start[1]+1), '-')
>>> connection_b.arcto((trace_start[0]+3, trace_start[1]+4), (trace_start[0]+1, trace_start[1]+4), '+')
>>> connection_b.lineto((trace_start[0]+3, trace_start[1]+6))
>>> top.add_traces_path(connection_b, trace_width, 'Conductor')
>>> top.add_pad(via_pad, (trace_start[0]+3, trace_start[1]+6), 0)
>>>
>>> # Write gerber file (to null device because this is a doctest)
>>> import os
>>> with open(os.devnull, 'w') as null_device:
...     top.dump_gerber(null_device)

This gerber file creates the following image:

.. image:: doctest_synthetic.png
    :width: 800
    :alt: Image generated by doctest artificial example

    
A PCB Profile
-------------

>>> from gerber_writer import (DataLayer, Path, set_generation_software)
>>>     
>>> set_generation_software('Karel Tavernier', 'gerber_writer_example_outline.py', '2022.06')    
>>> profile_layer = DataLayer('Profile,NP')    
>>> profile = Path()
>>> profile.moveto((0, 0))
>>> profile.lineto((150, 0))
>>> profile.arcto((160, 10), (160, 0), '-')
>>> profile.lineto((170, 10))
>>> profile.lineto((170, 90))
>>> profile.lineto((160, 90))
>>> profile.arcto((150, 100), (160, 100), '-')
>>> profile.lineto((0, 100))
>>> profile.lineto((0, 0))
>>> profile_layer.add_traces_path(profile, 0.5, 'Profile')
    
The Gerber output files creates the following image:

.. image:: doctest_outline.png
    :width: 800
    :alt: Image generated by doctest outline example
    
   
Use of NamedTuple
-----------------

Points in the plane are consistently represented as a Tuple[float, float].
The user can define his own NamedTuple and use it with this API:

>>> from gerber_writer import Circle, DataLayer
>>> from typing import NamedTuple
>>> class Pnt(NamedTuple):
...     x: float
...     y: float
>>> via = Circle(0.1, 'ViaPad')
>>> copper_bot = DataLayer('Copper,L4,Bot')
>>> origin = Pnt(0, 0)
>>> copper_bot.add_pad(via, origin)
    
    
    
Main Classes Reference
======================
"""
# Author:  Karel Tavernier
# Purpose: Generating Gerber files from PCB layout data
# Created: 2022 03 24
# Copyright: Karel Tavernier
# License: Apache 2.0 License

from collections import deque
from math import sqrt, sin, cos, acos, radians
from typing import NamedTuple, Set, Dict, List, Tuple, Deque
import types

# adf  #todo check if import math is needed
import math
from .lutils import report_with_line, isreal
# import inspect    # for debug reporting

from .__init__ import __version__
from .padmasters import (
    Circle,
    Rectangle,
    RoundedRectangle,
    ChamferedRectangle,
    Thermal,
    RoundedThermal,
    RegularPolygon,
    UserPolygon
    )

_generation_software = types.SimpleNamespace(vendor='', application='', version='')
"""The application generating the gerber file."""

# Utilities
# ---------

Point = Tuple[float, float]
"""Point in 2D image plane."""

# adf
def _pnt_max(a: Point , b: Point ) -> Point :
    """return maxima of the elements per index and return them as a point   """
    return (max(abs(a[0]), abs(b[0])), max(abs(a[1]), abs(b[1])))
# end adf

def _pnt_offset(a: Point, b: Point) -> Point:
    """ Return a tuple with offset or a - b"""
    return (a[0] - b[0], a[1] - b[1])
            
def _pnt_rotate(point: Point, angle: float) -> Point:
    """Return a point rotated around over angle, in degrees."""
    return (
        point[0]*cos(radians(angle)) - point[1]*sin(radians(angle)),
        point[0]*sin(radians(angle)) + point[1]*cos(radians(angle))
        )

def _pnt_linf(a: Point, b: Point) -> float:
    """Return Linf distance
    >>> from gerber_writer.writer import _pnt_linf
    >>> _pnt_linf((0, 0), (1, -2.3))
    2.3
    
    """
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
    
def _pnt_l2(a: Point, b: Point) -> float:
    """Return L2 or Euclidian distance
    >>> from gerber_writer.writer import _pnt_l2
    >>> _pnt_l2((0, 0), (3, -4))
    5.0
    
    """
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    
def _pnt_orientation(center: Point, p0: Point, p1: Point) -> str:
    """Return orientation of segment (p0, p1) viewed from center
    >>> from gerber_writer.writer import _pnt_orientation
    >>> _pnt_orientation((1, 1), (1, 2), (2, 2))
    '-'
    
    """
    value = (-(p0[1] - center[1])*(p1[0] - center[0]) + (p0[0] - center[0])*(p1[1] - center[1]))
    if value > 0:
        return '+'
    elif value == 0:
        return '0'
    elif value < 0:
        return '-'
    
def _santize_field(field: str) -> str:
    """Return string sanitized to comply with Gerber field syntax.
    
    Remove leading and trailing spaces and substitute characters '*%,' with '_'.
    """
    return field.translate(field.maketrans('*%,', '___')).strip()

# Private ancillary classes
# -------------------------

class _MoveTo(NamedTuple):
    """Path construction operator. Move current point.
    
    Sets current point, no other action.
    :param Point to:    Set current point to 'to'
    """
    
    to: Point
  
class _LineTo(NamedTuple):
    """Path construction operator. Draw linear segment.
    
    Draw linear segment from current point to end point.
    :param Point to:    End point of line segment
    ."""
    
    to: Point
                    
class _ArcTo(NamedTuple):
    """Path construction operator. Draw circular arc segment

    Draw circular arc segnent from current point to end point.
    If the start- and end-point coincide, it is a full, 360 degree arc.
    :param Point to: End point of arc 
    :param Point center: Center point of arc
    :param str orientation:  Arc orientation, either '+' or '-'
    """

    to: Point
    center: Point
    orientation: str
    
 
# Public attributes
# =================

def set_generation_software(vendor: str, application: str, version: str):
    """Add a statement in the Gerber file that identifies the software aaplication generating it.
    
    :param str vendor: The name of the vendor (or developer, IP onwner, project ...)
    :param str application: The name of the application itslelf
    :param str version: The version id of the application
    
    For more information see the Gerber layer format specification_ section 5.6.7
     
    :Example:
    
    >>> import gerber_writer
    >>> gerber_writer.set_generation_software('KiCad', 'Pcbnew', '(2017-02-08 revision 0dc1193)-master')
     
    """
    _generation_software.vendor = _santize_field(vendor)
    _generation_software.application = _santize_field(application)
    _generation_software.version = _santize_field(version)
  
class Path:
    """Curves that can be filled to create regions or stroked to create traces.
    
    Paths are used to define traces and regions (copper pours).    
    A path is composed of straight  and circular arc line segments, 
    which may connect to one another or may be disconnected. 
    A pair of segments are said to connect only if they are defined consecutively,
    with the second segment starting where the first one ends.
    Thus, the order in which the segments of a path are defined is significant.
    Nonconsecutive segments that meet or intersect fortuitously are not considered to connect.
    A path is made up of one or more disconnected subpaths, each comprising a sequence of connected segments.
    
    In general, the topology of the path is unrestricted: it may be concave or convex, may contain 
    multiple subpaths representing disjoint areas, and may intersect itself in arbitrary ways.
    
    However, when used to define regions, there are restrictions. 
    The main one is that all subpaths must be closed contours,
    their end point must be equal to their start point.
    See the DataLayer.add_region method for more details.
    
    :example:
    
    >>> # Define a region with one contour.
    >>> from gerber_writer import Path
    >>> d_shape = Path()
    >>> d_shape.moveto((0, 0))
    >>> d_shape.lineto((1, 0))
    >>> d_shape.arcto((1 ,1), (1, 0.5), '+')
    >>> d_shape.lineto((0, 1))
    >>> d_shape.lineto((0, 0))
    >>> len(d_shape)
    5
    
    """
    
    def __init__(self):
        self.operators: Deque = deque()  # Sequence of path construction operators
        self.current_point = None
        self.start_point = None
        self.contour = False
# adf 230915
        self.pointMax = (1, 1)

    def __len__(self) -> int:
        """Return number of construction operators."""
        return len(self.operators)
        
    def __repr__(self) -> str:
        return self.operators.__repr__()
        
    def moveto(self, to: Point):
        """Construction operator. Move the current point and start new subpath.
        
        :param Point to: start point of next subpath        
        """
        if not isinstance(to, tuple):
            raise TypeError('to must be a tuple of two floats')
        self.operators.append(_MoveTo(to))
        self.current_point = to
        self.start_point = to
        self.contour = False
# adf
        self.pointMax = _pnt_max(to, self.pointMax)
    
    def lineto(self, end: Point):
        """Construction operator. Add straight line segment from current point to end point to the current subpath.
        
        :param Point end: end point of added segment
        """
        if not isinstance(end, tuple):
            raise TypeError('end must be a tuple of two floats')
        if self.current_point == None: raise ValueError('no current point')
        self.operators.append(_LineTo(end))
        self.current_point = end
        if end == self.start_point:
            self.contour = True
        else:
            self.contour = False
# adf
        self.pointMax = _pnt_max(end, self.pointMax)

    def arcto(self, end: Point, center: Point, orientation: str):
        """Construction operator. Add circular arc segment from current point to end point to the current subpath.
        
        :param Point end: end point of added segment   
        :param Point center: center point of arc        
        :param str orientation: arc orientation, either '+' or '-'          
        """
        if not isinstance(end, tuple):
            raise TypeError('end must be a tuple of two floats')
        if not isinstance(center, tuple):
            raise TypeError('center must be a tuple of two floats')
        if not ((orientation == '+') or (orientation == '-')):
            raise ValueError('orientation must be "+" or "-"')
        if self.current_point == None: raise ValueError('no current point')
        MAX_DEVIATION = 2.0e-5
        if abs(_pnt_l2(center, self.current_point) - _pnt_l2(center, end)) > MAX_DEVIATION:
            raise ValueError(f'radii to begin and end points differ by more than {MAX_DEVIATION}')
        self.operators.append(_ArcTo(end, center, orientation))
        self.current_point = end
# adf 230913
        if end == self.start_point:
            self.contour = True
        else:
            self.contour = False
# adf
        self.pointMax = _pnt_max(end, self.pointMax)

class DataLayer:
    """Accumulate the graphics objects of a PCB layer, when complete output it as Gerber file.
    
    :param str function: Function of the layer e.g. 'Soldermask,Bot'. See .FileFunction values in the Gerber specification.
    :param bool negative: Polarity, negative if True, positive if False (default) 
    
    **DataLayer Methods Overview:**
    
    * **__init__**      - Set layer attributes function and polarity
    * **__repr__**      - Return a display of the attributes and the list of graphics objects
    * **__len__**       - Return the number of graphics objects in the DataLayer instance 
    * **add_pad**       - Add a pad to the DataLayer instance 
    * **add_trace_line** - Add a straight line trace to the DataLayer instance
    * **add_trace_arc** - Add a circulare are trace to the DataLayer instance
    * **add_trace_Path** - Add traces to the DataLayer instance by stroking a Path
    * **add_region**    - Add a region to the DataLayer instance
    * **dumps_gerber**  - Return a Gerber string representing the DataLayer instance
    * **dump_gerber**   - Write a Gerber file representing the DataLayer instance

    **DataLayer Methods Reference:**

    """

    class _Pad(NamedTuple):
        """A pad graphics object.
        
        Construct the pad by replicating the pad master at position, rotated over angle.
        
        >>> viapad = DataLayer._Pad(Rectangle(5.08, 2.54, 'SMDPad,CuDef'), (0, 0), 45)
        >>> viapad.master.function
        'SMDPad,CuDef'
        
         """
        
        master: object
        position: Point
        angle: float

    class _Region(NamedTuple):
        """Region graphics object.
        
        A regions is filled Path object, where all subpaths, called contours, are closed. 
        
        :param Path path: The path containing the contours.
        :param str function:  The function of the region
        :param bool negative:  The region is negative if True, positive if False (default)

        """
        
        path: Path
        function: str
        negative: bool=False

    class _TracesPath(NamedTuple):
        """A combined graphics objects made by stroking a Path instance."""
        
        path: Path
        width: float
        function: str
        negative: bool = False
            
    def __init__(self, function: str, negative=False):
        """Initialize DataLayer.
        
        Arguments:
        :param str function: The file function, e.g. 'SolderMask,Top'. See section 5.6.3 of the Gerber spec.
        :param bool negative: True if file is negative. The default is positive.
        
        For more information about valid file functions see the Gerber layer format specification_ section 5.6.3. 
        The initial DataLayer has an empty graphics object list and generation_software not set.
        
        """
        self.function = function
        self.negative = negative
        self.g_o_stream: List = list()
# adf
        self.pointMax = (1, 1)
        self.integerdigits = (0,0)

    def __repr__(self):
        """DataLayer attributes and list of graphics objects.
        
        >>> test = DataLayer('Other,test')
        >>> test.add_pad(Circle(1, 'Other,test'), (0,0))
        >>> test.__repr__()
        "function: Other,test\nnegative: False\n_Pad(master=Circle(diameter=1, function='Other,test', negative=False), position=(0, 0), angle=0)"
        
        """
        
        lines = []
        lines.append(f'function: {self.function}')
        lines.append(f'negative: {self.negative}')
        for g_o in self.g_o_stream: 
            lines.append(repr(g_o))
        return '\n'.join(lines)

    def __len__(self) -> int:
        """Return the number of graphics objects in the DataLayer instance.
        
        >>> test = DataLayer('Other,test')
        >>> len(test)
        0
        >>> test.add_pad(Circle(1, 'Other,test'), (0,0))
        >>> len(test)
        1
        
        """
        
        return len(self.g_o_stream)
   
    def add_pad(self, master, position: Point, angle: float=0):
        """Add a pad graphics object to the DataLayer instance.
        
        :param master: The pad master, which defines the pad shape, function and whether it is negative.
        :param Tuple[float, float] position: The point where the pad master is replicated.
        :param float angle: The rotation angle under which the pad master is replicated. Default 0.
        
        :Example:
        
        >>> top = DataLayer('Copper,L1,Top')
        >>> via_pad = Circle(0.254, 'ViaPad')
        >>> smd_pad = Rectangle(1, 3, 'SMDPad,CuDef')
        >>> top.add_pad(via_pad, (1.5, -2.5))
        >>> top.add_pad(via_pad, (2.5, -2.5))        
        >>> top.add_pad(smd_pad, (5, -2.5), 45)        
        
        """
        if not isinstance(master.function, str):
            raise ValueError('function must be string')        
        if not isinstance(position, tuple):
            raise ValueError('position must be a tuple of two float coordinates')
        if not isreal(angle):
            raise TypeError('angle must be int or float')                        
        # to be expanded with real checks on function, probably using regex
        self.g_o_stream.append(DataLayer._Pad(master, position, angle))

# adf
        report_with_line(f'line has position {position} and datalayer has max {self.pointMax}')
        self.pointMax = _pnt_max(position, self.pointMax)
        report_with_line(f'new max is  {self.pointMax}')
    
    def add_trace_line(self, start: Point, end: Point, width: float, function: str, negative: bool=False):
        """Add straight line trace to DataLayer.
        
        :param Tuple[float, float] start: Start point of the line segment
        :param Tuple[float, float] end: End point of the line segment
        :param float width: Width of the line segment
        :param str function: Function of the line segment, e.g. 'Conductor'
        :param bool negative: The line is negative if True, positive if False; default positive
        
        :Example:
        
        >>> top = DataLayer('Copper,L1,Top')
        >>> top.add_trace_line((0, 0), (1, 1), 0.1, 'Other,Test', False)
        
        """
        if not isinstance(start, tuple):
            raise TypeError('start is not a tuple')
        if not isinstance(end, tuple):
            raise TypeError('end is not a tuple')      
        if not isinstance(function, str):
            raise TypeError('function is not a str')
        if not isinstance(negative, bool):
            raise TypeError('negative is not bool')     
        if not isreal(width):
            raise TypeError('Width is not int or float')
        if width<0:
            raise ValueError('width is not >= 0')
        
        line = Path()
        line.moveto(start)
        line.lineto(end)      
        self.g_o_stream.append(DataLayer._TracesPath(line, width, function, negative))
# adf
        report_with_line(f'line has max {line.pointMax} and datalayer has {self.pointMax}')
        self.pointMax = _pnt_max(line.pointMax, self.pointMax)
        report_with_line(f'new max is  {self.pointMax}')

    def add_trace_arc(self, start: Point, end: Point, center: Point, orientation: str, width: float, function: str, negative: bool=False):
        """Add circular arc trace to DataLayer.
        
        :param Tuple[float, float] start: Start point of the arc segment
        :param Tuple[float, float] end: End point of the arc segment
        :param Tuple[float, float] center: Center of the arc segment
        :param str orientation: Orientation of the arc segment, either '+' or '-'
        :param float width: Width of the line segment
        :param str function: Function of the line segment, e.g. 'Conductor'
        :param bool negative: The line is negative if True, positive if False; default positive.
        
        :Example:
        
        >>> top = DataLayer('Copper,L1,Top')
        >>> top.add_trace_arc((0, 0), (1, 1), (1, 0), '-', 0.1, 'Other,Test')        
        
        """
        if not isinstance(start, tuple):
            raise TypeError('start is not a tuple')
        if not isinstance(end, tuple):
            raise TypeError('end is not a tuple')
        if not isinstance(center, tuple):
            raise TypeError('center is not a tuple')                 
        if not isinstance(function, str):
            raise TypeError('function is not str')
        if not isinstance(negative, bool):
            raise TypeError('negative is not bool')     
        if not isreal(width):
            raise TypeError('Width is not int or float')
        if width<0:
            raise ValueError('width is not >= 0')
        arc = Path()
        arc.moveto(start)
        arc.arcto(end, center, orientation)      
        self.g_o_stream.append(DataLayer._TracesPath(arc, width, function, negative))
# adf
        report_with_line(f'trace_arc has max {arc.pointMax} and datalayer has {self.pointMax}')
        self.pointMax = _pnt_max(arc.pointMax, self.pointMax)
        report_with_line(f'new max is  {self.pointMax}')
        
    def add_traces_path(self, path: Path, width: float, function: str, negative: bool=False):
        """Add traces by stroking a path.
        
        :param Path path: The path that is to be stroked to create sequences of line and arc traces
        :param float width: Width of the traces
        :param str function: Function of the traces
        :param bool negative: The region is negative if True, positive if False; default positive
        
        :Example:
        
        >>> from gerber_writer import DataLayer, Path
        >>> copper_top = DataLayer('Copper,L1,Top')        
        >>> connection = Path()
        >>> connection.moveto((0, 0))
        >>> connection.lineto((1, 0))
        >>> connection.arcto((1 ,1), (1, 0.5), '+')
        >>> copper_top.add_traces_path(connection, 0.1, 'Conductor')
        >>> len(copper_top)
        1
        
        """        
        if not isinstance(path, Path):
            raise TypeError('path is not a Path instance')
        if not isreal(width):
            raise TypeError('width is not int or float')
        if width<0:
            raise ValueError('width is not >= 0')
        if not isinstance(function, str): 
            raise TypeError('function is not str')        
        if not isinstance(negative, bool):
            raise TypeError('negative flag is not bool')        
        self.g_o_stream.append(DataLayer._TracesPath(path, width, function, negative))
# adf
        report_with_line(f'line has max {path.pointMax} and datalayer has {self.pointMax}')
        self.pointMax = _pnt_max(path.pointMax, self.pointMax)
        report_with_line(f'new max is  {self.pointMax}')
        
    def add_region(self, path: Path, function: str, negative: bool=False):
        """Add a region graphics object to the DataLayer.
        
        :param Path path:  The path object whose subpaths are the contours describing the region
        :param str funcion: The function of the region, e.g. 'Conductor
        :param bool negative: The region is negative if True, positive if False (default)
        
        :Example:
        
        >>> from gerber_writer import DataLayer, Path
        >>> copper_top = DataLayer('Copper,L1,Top')        
        >>> d_shape = Path()
        >>> d_shape.moveto((0, 0))
        >>> d_shape.lineto((1, 0))
        >>> d_shape.arcto((1 ,1), (1, 0.5), '+')
        >>> d_shape.lineto((0, 1))
        >>> d_shape.lineto((0, 0))
        >>> copper_top.add_region(d_shape, 'Conductor')
        >>> len(copper_top)
        1
        
        The fundamental requirement for regions is that all subpaths must be closed,
        meaning that their end point exactoy coincides with the start point.
        Furthermore, the contours cannot be self-intersecting.
        For more information about valied contours see the Gerber Layer Fo(rmat specification _ section 4.10.3. 
        
        """
        if not isinstance(path, Path): raise TypeError('path is not a Path instance')
        if not isinstance(function, str): raise TypeError('function is not str')        
        if not isinstance(negative, bool): raise TypeError('negative flag is not bool')        
        if path.contour == False: raise ValueError('some subpaths are not closed')
        self.g_o_stream.append(DataLayer._Region(path, function, negative))
# adf
        self.pointMax = _pnt_max(path.pointMax, self.pointMax)
        report_with_line(f'(x_max, y_max):   {path.pointMax}' )

    def dumps_gerber(self) -> str:
        '''Return a string in Gerber format representing the DataLayer.'''
        
        # Load macros that are used to create pads
        from . macros import (
            _MACRO_RECTANGLE,
            _MACRO_ROUNDED_RECTANGLE,
            _MACRO_CHAMFERED_RECTANGLE,
            _MACRO_THERMAL,
            _MACRO_ROUNDED_THERMAL
            )
        import datetime    
        import itertools
        
        TO_NM = 1_000_000  # convert user units (mm) to gerber coordinates (nm)
        DECIMALS = 6  # Max number of decimals in calculated Gerber AD parameters
        TOLERANCE = 0.5e-3  # Smaller features can be simplified for a more robust Gerber file   
        
        graphics_state = types.SimpleNamespace(point=None, dcode=None, g0n=None, negative=None)
        macros: Set[str] = set() # set with all used macro's
        apertures: Dict = dict() # dict with all created apertures
        polygons: Dict = dict() # dict with all user defined polygon masters
        
        ad_commands: List = list()
        body_commands: List = list()  # G01/2/3, %LP, Dnn, D01/01/03, G37/37...
        
        generate_dcode = itertools.count(10) # start at 10 per Gerber spec on dcodes
        generate_polygon_number = itertools.count(1) # start at one for human readability
 
        # Point functions
            
        def _pnt_gerber(point: Point) -> Point:
            """Return a point in gerber coordinate units (nm)."""
            return (int(point[0]*TO_NM), int(point[1]*TO_NM))
        
        # Functions to LP, G01/2/3, D code, D02

        def handle_g0n(plotmode: str):
            """Output G01/2/3 command when needed and set graphics state."""
            if graphics_state.g0n != plotmode:
                body_commands.append(plotmode)
                graphics_state.g0n = plotmode                

        def handle_d02(point: Point):
            """Output D02 command when needed, set graphics state."""
            if graphics_state.point != point:                
                body_commands.append(
                    f'X{_pnt_gerber(point)[0]}'
                    f'Y{_pnt_gerber(point)[1]}'
                    f'D02*'
                    )
                graphics_state.point = point
                
        def handle_lp(negative: bool):
            """Output %LP when needed, set graphics state"""
            if graphics_state.negative != negative:
                body_commands.append(f'%LP{"C" if negative else "D"}*%')
                graphics_state.negative = negative             
            
        def handle_dcode(shape: str, function: str, negative: bool, ad_body: str):
            """Output Dnn when needed, generate AD when needed, set graphics state."""
            key = (shape, function, negative)
            dcode = apertures.get(key)
            if dcode is None:
                # Define dcode and its aperture
                dcode = next(generate_dcode)
                apertures[key] = dcode                
                if function != '': 
                    ad_commands.append(f'G04 #@! TA.AperFunction,{function}*')
                ad_commands.append(f'G04 #@! TAShape,{shape}*')
                ad_commands.append(f'%ADD{dcode}{ad_body}*%')
                if function != '':
                    ad_commands.append('G04 #@! TD*')
            if graphics_state.dcode != dcode:
                body_commands.append(f'D{dcode}*')
                graphics_state.dcode = dcode
                      
        def handle_flash(shape: str, ad_body: str):
            """Output all Gerber commands for a flash incl, LP, AD, Dnn."""
            handle_lp(graphics_object.master.negative)
            handle_dcode(
                shape,
                graphics_object.master.function,
                graphics_object.master.negative,
                ad_body
                )                   
            body_commands.append(
                f'X{_pnt_gerber(graphics_object.position)[0]}'
                f'Y{_pnt_gerber(graphics_object.position)[1]}'
                f'D03*'
                )
            graphics_state.point = graphics_object.position
            
        def handle_trace_lp_ad_dnn():
            """Output LP, AD, Dnn as needed before the d01, d02."""
            handle_lp(graphics_object.negative)
            shape = f'Circle,{graphics_object.width}'
            ad_body = f'C,{graphics_object.width}'
            handle_dcode(
                shape,
                graphics_object.function,
                graphics_object.negative,
                ad_body
                )
                
        def handle_path_operators(path: Path, always_d02: bool):
            """Output all d01 and d02 as required by the path operators.
            
            :param Path path: the path that contains the operators.
            :param bool always_do2: if True always generate the d02
                                    even when not needed by current state
                                    d02 is mandatory at the start of a contour
            """
            for operator in path.operators:
                if isinstance(operator, _MoveTo):
                        if always_d02:
                            body_commands.append(
                                f'X{_pnt_gerber(operator.to)[0]}'
                                f'Y{_pnt_gerber(operator.to)[1]}'
                                f'D02*'
                                )                                   
                        else:
                            handle_d02(operator.to)
                        
                elif isinstance(operator, _LineTo):            
                        handle_g0n('G01*')
                        body_commands.append(
                            f'X{_pnt_gerber(operator.to)[0]}'
                            f'Y{_pnt_gerber(operator.to)[1]}'
                            f'D01*'
                            )
                            
                elif isinstance(operator, _ArcTo):
                        if operator.orientation == '+':
                                handle_g0n('G03*')
                        elif operator.orientation == '-':
                                handle_g0n('G02*')
                        else:
                                assert False, 'Orientation must be "+" or "-" '
                        chord_short = _pnt_linf(graphics_state.point, operator.to) < TOLERANCE/2
                        arc_small = _pnt_orientation(operator.center, graphics_state.point, operator.to) == operator.orientation
                        radius_long = _pnt_linf(operator.center, operator.to) > TOLERANCE
                        if chord_short and arc_small and radius_long:
                            # Output as line instead of arc segment to avoid instability
                            body_commands.append(
                                f'X{_pnt_gerber(operator.to)[0]}'
                                f'Y{_pnt_gerber(operator.to)[1]}'
                                f'D01*'
                                )
                        else:
                            # Output as arc
                            body_commands.append(
                                f'X{_pnt_gerber(operator.to)[0]}'
                                f'Y{_pnt_gerber(operator.to)[1]}'
                                f'I{_pnt_gerber(_pnt_offset(operator.center, graphics_state.point))[0]}'
                                f'J{_pnt_gerber(_pnt_offset(operator.center, graphics_state.point))[1]}'                                                            
                                f'D01*'
                                )
                            
                else:
                        assert False, 'Unknown path construction operator'

                graphics_state.point = operator.to
        
        # Process graphics objects:
        # compute macro and aperture dicts, AD and operation command list        
        for graphics_object in self.g_o_stream:        
            # match graphics_object:
            if isinstance(graphics_object, DataLayer._TracesPath):
                    handle_trace_lp_ad_dnn()
                    handle_path_operators(graphics_object.path, always_d02=False)            
            
            elif isinstance(graphics_object, DataLayer._Region):
                    handle_lp(graphics_object.negative)
                    if graphics_object.function != '':                        
                        body_commands.append(f'G04 #@! TA.AperFunction,{graphics_object.function}*')                
                    body_commands.append('G36*')
                    handle_path_operators(graphics_object.path, always_d02=True)
                    body_commands.append('G37*')
                    if graphics_object.function != '':                            
                        body_commands.append('G04 #@! TD*')
            
            elif isinstance(graphics_object, DataLayer._Pad) and isinstance(graphics_object.master, Circle):
                    shape = f'Circle,{graphics_object.master.diameter}'
                    ad_body = f'C,{graphics_object.master.diameter}'
                    handle_flash(shape, ad_body)

            elif isinstance(graphics_object, DataLayer._Pad) and isinstance(graphics_object.master, Rectangle):
                    shape = (
                        f'Rectangle,'
                        f'{graphics_object.master.x_size},'
                        f'{graphics_object.master.y_size},'
                        f'{graphics_object.angle}'
                        )
                    if graphics_object.angle%180 == 0:
                        ad_body = (
                            f'R,'
                            f'{graphics_object.master.x_size}X'
                            f'{graphics_object.master.y_size}'
                            )
                    else:
                        macros.add(_MACRO_RECTANGLE)
                        ad_body = (
                            f'Rectangle,'
                            f'{graphics_object.master.x_size/2}X'
                            f'{graphics_object.master.y_size/2}X'
                            f'{graphics_object.angle}'          
                            )                                    
                    handle_flash(shape, ad_body)             

            elif isinstance(graphics_object, DataLayer._Pad) and isinstance(graphics_object.master, RoundedRectangle):
                    x_size = graphics_object.master.x_size
                    y_size = graphics_object.master.y_size                            
                    radius = graphics_object.master.radius
                    angle = graphics_object.angle
                    shape = f'RoundedRectangle,{x_size},{y_size},{radius},{angle}'
                    if ((min(x_size, y_size) - 2*radius) < TOLERANCE) and (angle%90==0):
                        # Becomes obround
                        ad_body = f'O,{x_size}X{y_size}'              
                    else:
                        macros.add(_MACRO_ROUNDED_RECTANGLE)
                        xc = x_size/2 - radius
                        yc = y_size/2 - radius
                        center_q1 = _pnt_rotate((+xc, yc), angle) # Center of 1st quadrant circle
                        center_q2 = _pnt_rotate((-xc, yc), angle) # Center of 2nd quadrant circle                         
                        ad_body = (
                            f'RoundedRectangle,'
                            f'{round(x_size/2, DECIMALS)}X'
                            f'{round(y_size/2, DECIMALS)}X'
                            f'{round(xc, DECIMALS)}X'
                            f'{round(yc, DECIMALS)}X'
                            f'{round(angle, DECIMALS)}X'
                            f'{round(2*radius, DECIMALS)}X'
                            f'{round(center_q1[0], DECIMALS)}X'
                            f'{round(center_q1[1], DECIMALS)}X'
                            f'{round(center_q2[0], DECIMALS)}X'
                            f'{round(center_q2[1], DECIMALS)}'
                            )
                    handle_flash(shape, ad_body)                  

            elif isinstance(graphics_object, DataLayer._Pad) and isinstance(graphics_object.master, ChamferedRectangle):
                    shape = (
                        f'ChamferedRectangle,'
                        f'{graphics_object.master.x_size},'
                        f'{graphics_object.master.y_size},'
                        f'{graphics_object.master.cutoff},'
                        f'{graphics_object.angle}'
                        )
                    macros.add(_MACRO_CHAMFERED_RECTANGLE)                           
                    ad_body = (
                        f'ChamferedRectangle,'
                        f'{graphics_object.master.x_size/2}X'
                        f'{graphics_object.master.y_size/2}X'
                        f'{graphics_object.master.x_size/2-graphics_object.master.cutoff}X'
                        f'{graphics_object.master.y_size/2-graphics_object.master.cutoff}X'
                        f'{graphics_object.angle}'
                        )
                    handle_flash(shape, ad_body)
                                                                     
            elif isinstance(graphics_object, DataLayer._Pad) and isinstance(graphics_object.master, Thermal):
                    shape = (
                        f'Thermal,'
                        f'{graphics_object.master.outer_diameter},'
                        f'{graphics_object.master.inner_diameter},'
                        f'{graphics_object.master.gap},'
                        f'{graphics_object.angle}'
                        )
                    macros.add(_MACRO_THERMAL)
                    ad_body = (
                        f'Thermal,'
                        f'{graphics_object.master.outer_diameter}X'
                        f'{graphics_object.master.inner_diameter}X'
                        f'{graphics_object.master.gap}X'
                        f'{graphics_object.angle}'
                        )
                    handle_flash(shape, ad_body)
                        
            elif isinstance(graphics_object, DataLayer._Pad) and isinstance(graphics_object.master, RoundedThermal):
                    shape = (
                        f'RoundedThermal,'
                        f'{graphics_object.master.outer_diameter},'
                        f'{graphics_object.master.inner_diameter},'
                        f'{graphics_object.master.gap},'
                        f'{graphics_object.angle}'
                        )
                    macros.add(_MACRO_ROUNDED_THERMAL)                                   
                    outer_diameter = graphics_object.master.outer_diameter
                    inner_diameter = graphics_object.master.inner_diameter
                    gap_given = graphics_object.master.gap
                    angle = graphics_object.angle
                    # Calculate parameters of primitives
                    # The cut of primitive 7 is not radial;
                    # consequentely the diameter of the rounding circles is larger than the gap, and they stick out
                    if gap_given*sqrt(2) >= (inner_diameter - (1 + sqrt(2))*(outer_diameter - inner_diameter)):
                        # Large gap; to make room circles must be on the cut and the circles stick out on both sides
                        gap_primitive = gap_given + (outer_diameter-inner_diameter)/2 # gap for primitive 7, 1st approximation
                        while True:
                            # Secant method iteration till error between given and constructed gap is less than tolerance/10
                            corner_y_inner = inner_diameter*sin(acos(gap_primitive/inner_diameter))/2
                            corner_y_outer = outer_diameter*sin(acos(gap_primitive/outer_diameter))/2
                            rounding_diameter = corner_y_outer - corner_y_inner
                            gap_real = gap_primitive - rounding_diameter
                            if abs(gap_given - gap_real) < TOLERANCE/10: break
                            gap_primitive += gap_given - gap_real
                        # calculate centers of rounding circles in 1st quadrant before rotation
                        center_h = _pnt_rotate(((corner_y_outer + corner_y_inner)/2, gap_primitive/2), angle) # circle along h axis
                        center_v = _pnt_rotate((gap_primitive/2, (corner_y_outer + corner_y_inner)/2), angle) # h axis                                  
                    else:
                        # overshoot to the interior, where it can be erased with the negative circle
                        gap_primitive = gap_given + 1.2*(outer_diameter-inner_diameter)/2 # gap for primitive 7, first approximation 
                        while True:
                            # Secant method iteration till error between given and constructed gap is less than tolerance/10
                            alfa_inner = acos(gap_primitive/inner_diameter)
                            alfa_outer = acos(gap_primitive/outer_diameter)                                                                            
                            corner_y_inner = inner_diameter*sin(alfa_inner)/2
                            corner_y_outer = outer_diameter*sin(alfa_outer)/2
                            rounding_diameter = (corner_y_outer - corner_y_inner)/sin(alfa_outer)
                            gap_real = gap_primitive - rounding_diameter*(1+cos(alfa_outer))
                            if abs(gap_given - gap_real) < TOLERANCE/10: break
                            gap_primitive += gap_given - gap_real                                 
                        # calculate centers of rounding circles in 1st quadrant before rotation
                        rounding_distance = outer_diameter - rounding_diameter
                        center_v = _pnt_rotate((rounding_distance*cos(alfa_outer)/2, rounding_distance*sin(alfa_outer)/2), angle) # circle along v axis
                        center_h = _pnt_rotate((rounding_distance*sin(alfa_outer)/2, rounding_distance*cos(alfa_outer)/2), angle) # circle along h axis
                    # Now we are ready to construct ad_body
                    ad_body = (
                        f'RoundedThermal,'
                        f'{outer_diameter}X'
                        f'{inner_diameter}X'
                        f'{round(gap_primitive, DECIMALS)}X'
                        f'{graphics_object.angle}X'
                        f'{round(rounding_diameter, DECIMALS)}X'
                        f'{round(center_h[0], DECIMALS)}X'
                        f'{round(center_h[1], DECIMALS)}X'           
                        f'{round(center_v[0], DECIMALS)}X'          
                        f'{round(center_v[1], DECIMALS)}'                                                   
                        )
                    handle_flash(shape, ad_body)
                    
            elif isinstance(graphics_object, DataLayer._Pad) and isinstance(graphics_object.master, RegularPolygon):
                    shape = (
                        f'RegularPolygon,'
                    f'{graphics_object.master.outer_diameter},'
                        f'{graphics_object.master.vertices},'
                        f'{graphics_object.angle}'
                        )
                    ad_body = (
                        r'P,'
                        f'{graphics_object.master.outer_diameter}X'
                        f'{graphics_object.master.vertices}X'
                        f'{graphics_object.angle}'
                        )
                    handle_flash(shape, ad_body)                            
                    
            elif isinstance(graphics_object, DataLayer._Pad) and isinstance(graphics_object.master, UserPolygon):
                    macro_name = polygons.get(graphics_object.master.polygon)
                    if macro_name is None: # polygon does not yet exist
                        # add polygon to polygons dict         
                        macro_name = f'UserPolygon_{next(generate_polygon_number)}'                                 
                        polygons[graphics_object.master.polygon] = macro_name
                        # define macro and add it to macros set                                                                 
                        macro_definition = []
                        macro_definition.append(f'%AM{macro_name}*')
                        macro_definition.append(f'4,1,{len(graphics_object.master.polygon)-1},')
                        macro_definition.extend([f'{point[0]},{point[1]},' for point in graphics_object.master.polygon])
                        macro_definition.append('$1*')
                        macro_definition.append('%')
                        macros.add('\n'.join(macro_definition))                       
                    shape = f'UserPolygon,{graphics_object.angle}'
                    ad_body = f'{macro_name},{graphics_object.angle}'
                    handle_flash(shape, ad_body)
                        
            else:
                assert False, 'Unknown graphics object'

        # Construct list of all commands
        # Header
        all_commands: List = list() # Stream of all commands that will be in the Gerber file
        all_commands.append(f'G04 Created with the python gerber_writer {__version__}*')
        all_commands.append(f'G04 #@! TF.CreationDate,{datetime.datetime.now().isoformat()}*')
        if self.function != '':
            all_commands.append(f'G04 #@! TF.FileFunction,{self.function}*')
        if self.negative == False:
            all_commands.append('G04 #@! TF.FilePolarity,Positive*')
        else:
            all_commands.append('G04 #@! TF.FilePolarity,Negative*')
        if not (_generation_software.vendor == _generation_software.application == _generation_software.version == ''):
            all_commands.append(
                f'G04 #@! TF.GenerationSoftware,'
                f'{_generation_software.vendor},'
                f'{_generation_software.application},'
                f'{_generation_software.version}*'
                )
        all_commands.append('%MOMM*%')
# adf 230918
        self.integerdigits = (max(1 + int(math.log10(self.pointMax[0])), 3), max(1 + int(math.log10(self.pointMax[1])), 3))
        report_with_line(f'(x_integerdigits, y_integerdigits) = {self.integerdigits}')

# adf
        # all_commands.append('%FSLAX36Y36*%')
        max_integerdigits = max(self.integerdigits[0], self.integerdigits[1])
        all_commands.append(f'%FSLAX{max_integerdigits}6Y{max_integerdigits}6*%')
# end adf
        all_commands.append('G75*')
        # Macro commands
        all_commands.extend(sorted(macros)) # sort to have a predicatable order for unittest
        # AD commands
        all_commands.extend(ad_commands)
        # Body commands (D01/02/03, G01/02/03, G36/G37)
        all_commands.extend(body_commands)
        # End of file
        all_commands.append('M02*')

# karel wil dit niet wheee
        # print(f'\nthe size of this gerber is {self.pointMax[0]:.3f} X {self.pointMax[1]:.3f}')

        return '\n'.join(all_commands)

    def dump_gerber(self, gerber_file):
        """Write a gerber file representing the DataLayer.
        
        :param file_object gerber_file: The output Gerber file
        """

        gerber_file.write(self.dumps_gerber())
            
