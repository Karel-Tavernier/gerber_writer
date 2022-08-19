""" 
Padmaster Classes Reference
---------------------------

A padmaster has the following attributes:

* shape:    Geometric shape, e.g. rectangle
* function: A pad function, e.g. 'ViaPad'
* polarity: Positive or negative

Padmasters are used to create pads by replicating them

* at a given point on the 2D plane
* under a given angle


"""

# Copyright:  Karel Tavernier
# Created: 2022 03 24
# Copyright: Karel Tavernier
# License: Apache 2.0 license
# 
# Revision history

from dataclasses import dataclass
from math import sqrt

@dataclass(frozen = True)
class Circle:
    """A pad master with circular shape.
    
    A pad master serves to add pads to the graphics objects list. It defines
    their geometric shape, function and polarity (positive or negative).
    The function attribute specifies what the funtions is of the pad, e.g. 'ViaPad' or 'ComponentPad'.
    See .AperFunction values in the Gerber format specification.

    :param float diameter: Diameter of the circular pads
    :param str function: Function of the pads e.g. 'ViaPad'
    :param bool negative: Polarity, negative if True, positive if False (default)
    """
    
    diameter: float
    function: str
    negative: bool = False
    def __post_init__(self):
        if not isinstance(self.diameter, float|int):
            raise TypeError('diameter must be int or float')
        if self.diameter <0 :
            raise ValueError('diameter must be >=0')
        if not isinstance(self.function, str):
            raise TypeError('function must be str')
        if not isinstance(self.negative, bool):
            raise TypeError('function must be bool')
        
@dataclass(frozen = True)
class Rectangle:
    """A pad master with an axis-aligned rectangular shape.
    
    :param float x_size: Size along x-axis
    :param float y_size: Size along y-axis
    :param str function: Function of the pads e.g. 'SMDPad,CuDef''
    :param bool negative: Polarity, negative if True, positive if False (default)    
    """
    
    x_size: float
    y_size: float
    function: str
    negative: bool = False
    def __post_init__(self):
        if not isinstance(self.x_size, float|int):
            raise TypeError('X size must be int or float')
        if self.x_size <= 0:
            raise ValueError('X size must be >=0')
        if not isinstance(self.y_size, float|int):
            raise TypeError('Y size must be int or float')
        if  self.y_size <= 0:
            raise ValueError('Y size must be >=0')
        if not isinstance(self.function, str):
            raise TypeError('Function must be str')
        if not isinstance(self.negative, bool):
            raise TypeError('Function must be bool')
    
@dataclass(frozen=True)
class RoundedRectangle:
    """A pad master, an ax-s-aligned rectangle with rounded corners.
    
    :param float x_size: Size along x-axis
    :param float y_size: Size along y-axis
    :param float radius: Radius of the corner rounding    
    :param str function: Function of the pads e.g. 'SMDPad,CuDef''
    :param bool negative: Polarity, negative if True, positive if False (default)    
    """
    
    x_size: float
    y_size: float
    radius: float
    function: str
    negative: bool = False
    def __post_init__(self):
        if not isinstance(self.x_size, float|int):
            raise TypeError('x_size must be int or float')
        if self.x_size <= 0:
            raise ValueError('x_size must be >0')
        if not isinstance(self.y_size, float|int):
            raise TypeError('y_size must be int or float')
        if  self.y_size <= 0:
            raise ValueError('y_size must be >0')
        if not isinstance(self.radius, float|int):
            raise TypeError('radius must be int or float')
        if not (0 <= self.radius <= 0.5*min(self.x_size, self.y_size)):
            raise ValueError('radius must be: 0 <= radius <= half the smallest side')            
        if not isinstance(self.function, str):
            raise TypeError('function must be str')
        if not isinstance(self.negative, bool):
            raise TypeError('Function must be bool')
        
@dataclass(frozen = True)
class ChamferedRectangle:
    """A pad master, an axis-aligned rectangle with chamfered corner.
    
    :param float x_size: Size along x-axis
    :param float y_size: Size along y-axis
    :param float cutoff: Cutoff distance from corner for the chamfer
    :param str function: Function of the pads e.g. 'SMDPad,CuDef'
    :param bool negative: Polarity, negative if True, positive if False (default)
    """
    
    x_size: float
    y_size: float
    cutoff: float
    function: str
    negative: bool = False
    def __post_init__(self):
        if not isinstance(self.x_size, float|int):
            raise TypeError('X size must be int or float')
        if self.x_size <= 0:
            raise ValueError('X size must be >=0')
        if not isinstance(self.y_size, float|int):
            raise TypeError('Y size must be int or float')
        if  self.y_size <= 0:
            raise ValueError('Y size must be >=0')
        if not isinstance(self.cutoff, float|int):
            raise TypeError('Cutoff must be int or float')
        if not (0 <= self.cutoff <= 0.5*min(self.x_size, self.y_size)):
            raise ValueError('Cutoff must be: 0 <= cutoff <= half the smallest side')            
        if not isinstance(self.function, str):
            raise TypeError('Function must be str')

@dataclass(frozen=True)      
class Thermal:
    """A pad master, circular thermal with four axis-aligned straight gap openings.
    
    :param float outer_diameter: Outer diameter of the thermal
    :param float inner_diameter: Inner diameter of the thermal
    :param float gap: Gap or conductor width beteen thermal barriers along the axis
    :param str function: Function of the pads e.g. 'ThermalReliefPad'
    :param bool negative: Polarity, negative if True, positive if False (default)
    """
    
    outer_diameter: float
    inner_diameter: float
    gap: float
    function: str
    negative: bool = False
    def __post_init__(self):
        if not (isinstance(self.outer_diameter, int|float) and isinstance(self.inner_diameter, int|float) and isinstance(self.gap, int|float)):
            raise TypeError('arguments must be int or float')
        if not (0 < self.inner_diameter < self.outer_diameter):
            raise ValueError('diameter values invalid')
        if not(0 < self.gap < self.outer_diameter/sqrt(2)):
            raise ValueError('gap only valid if 0 < gap <= outer_diameter/math.sqrt(2)')
            
@dataclass(frozen=True)      
class RoundedThermal:
    """A pad master, circular thermal with four axis-aligned rounded gap openings.
    
    :param float outer_diameter: Outer diameter of the thermal
    :param float inner_diameter: Inner diameter of the thermal
    :param float gap: Gap or conductor width beteen thermal barriers along the axis
    :param str function: Function of the pads e.g. 'ThermalReliefPad'
    :param bool negative: Polarity, negative if True, positive if False (default)   
    """
    
    outer_diameter: float
    inner_diameter: float
    gap: float
    function: str
    negative: bool = False
    def __post_init__(self):
        if not (isinstance(self.outer_diameter, int|float) and isinstance(self.inner_diameter, int|float) and isinstance(self.gap, int|float)):
            raise TypeError('arguments must be int or float')
        if not (self.outer_diameter>0 and self.inner_diameter>0 and self.gap>0):
            raise ValueError('parameters must be strictly positive')
        if (self.gap + self.outer_diameter - self.inner_diameter)*2*sqrt(2) >= (self.outer_diameter + self.inner_diameter): # for simpler rounding
#        if self.gap*sqrt(2) >= (self.inner_diameter - (1 + sqrt(2))*(self.outer_diameter - self.inner_diameter)):
            raise ValueError('gap too big in relation to diameters')
            
@dataclass(frozen=True)
class RegularPolygon:
    """A pad master, with shape a regular convex polygon.
    
    One vertex is on the positive x-axis.
    
    :param float outer_diameter: Outer diameter, or diameter of the circumscribed circle
    :param int vertices: Number of vertices
    :param str function: Function of the pads e.g. 'FiducialPad,Local'
    :param bool negative: Polarity, negative if True, positive if False (default)       
    """
    
    outer_diameter: float
    vertices: int
    function: str
    negative: bool = False
    def __post_init__(self):
        if not isinstance(self.outer_diameter, float|int):
            raise TypeError('outer_diameter must be int or float')
        if self.outer_diameter <= 0:
            raise ValueError('outer_diameter must be >=0')
        if not isinstance(self.vertices, int):
            raise TypeError('vertices must be int or float')
        if self.vertices not in range(3,13) :
            raise ValueError('vertices must be from 3 up to 12')         
        if not isinstance(self.function, str):
            raise TypeError('function must be str')
        if not isinstance(self.negative, bool):
            raise TypeError('Function must be bool')
        
@dataclass(frozen=True)
class UserPolygon:
    """A pad master with a user defined shape.
    
    The shape is defined by its polygon outline or contour
    The outline must be closed: the last vertex must coincide with the first one.
    For more information about valied contours see the Gerber Layer Format specification _ section 4.10.3.
    The reference point, this is the point used to put the pad in the plane with add_pad, is the origin
    of the coordinate system used to define the outline
    
    :param int polygon: A tuple with the vertices of the polygon;  each vertex is a tuple (x, y)
    :param str function: Function of the pads e.g. 'TestPad'
    :param bool negative: Polarity, negative if True, positive if False (default)  
    """
    
    polygon: tuple
    function: str
    negative: bool = False
    def __post_init__(self):
        if not isinstance(self.polygon, tuple):
            raise TypeError('polygon must be tuple of points')
        if len(self.polygon) <3:
            raise ValueError('polygon must have at least three vertices')
        if self.polygon[0] != self.polygon[-1]:
            raise ValueError('polygon must be closed')     
        if not isinstance(self.function, str):
            raise TypeError('function must be str')
        if not isinstance(self.negative, bool):
            raise TypeError('Function must be bool')

           
# Run doctest when called as main
if __name__ == "__main__":
    import doctest
    doctest.testmod()