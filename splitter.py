# This splits a geometric object into points and take a series of [x, y] coordinates and splits them into a list of points.
from Point import Point
import draw
import math
from typing import List, Tuple, Dict, Optional, Set


class ShapeDataStructure:
    def __init__(self, width, height, resolution=1):
        self.width = width
        self.height = height
        self.resolution = resolution
        
        # Create grid of all possible points
        self.grid: Dict[Tuple[float, float], Point] = {}
        self._initialize_grid()
        
        # Track drawn points in a set because we use this to do lookups
        self.drawn_points: Set[Point] = set()

    def set_up_points(coordinates, resolution = 1):
        """Splits a series of [x, y] coordinates into a list.
    """
        points = []
        for coord in coordinates:
            x, y = coord
            points.append(Point(x, y, ))
            #point_attributes(points)
            
        return points

    def point_attributes(point):
        """Assigns attributes to each point based on what surrounds it
        """
        # assign root
         #if point.coordinates == draw.get_origin_coords():
     #       point.attributes['root'] = True
           
        # assign planar
        # assign interior
        # assign exterior
        
        pass


    
        


