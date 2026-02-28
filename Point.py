
from enum import Enum
from typing import Optional

class PointType(Enum):
    ROOT = "root"              # x=0 point
    INTERIOR = "interior"       # 0 missing quadrants
    INTERIOR_CORNER = "interior_corner"  # 1 missing quadrant
    PLANAR = "planar"           # 2 missing quadrants
    EXTERIOR_CORNER = "exterior_corner"  # 3 missing quadrants
    EXTERIOR = "exterior"       # if we want to add air for some reason, 4 missing quadrants

class Quadrant(Enum):
    Q1 = "q1"  # (x+1, y-1)  # Northeast
    Q2 = "q2"  # (x-1, y-1)  # Northwest
    Q3 = "q3"  # (x-1, y+1)  # Southwest
    Q4 = "q4"  # (x+1, y+1)  # Southeast

class Point:
    def __init__(self, x: float, y: float, temperature: float = 20.0, material: Optional[str] = None):
        self.x = x
        self.y = y
        self.coordinates = (x, y)
        
        # Linked list connections (4-directional)
        self.right: Optional['Point'] = None   # Next point in +x direction
        self.left: Optional['Point'] = None    # Next point in -x direction
        self.up: Optional['Point'] = None      # Next point in -y direction (if y increases downward)
        self.down: Optional['Point'] = None    # Next point in +y direction

        # Quadrant connections (diagonals)
        self.q1: Optional['Point'] = None  # NE
        self.q2: Optional['Point'] = None  # NW
        self.q3: Optional['Point'] = None  # SW
        self.q4: Optional['Point'] = None  # SE

         # Point attributes as a dictionary
        self.attributes = {
            'type': None,           # PointType (exterior, interior, planar, root, corner)
            'root': False,          
            'temperature': 20.0,     # Current temperature
            'material': None,        # Material at this point
            'quadrants': {           # Which quadrants have adjacent points
                Quadrant.NE: False,
                Quadrant.NW: False,
                Quadrant.SE: False,
                Quadrant.SW: False
            },
            #'boundary_condition': None,  # maybe use this later if we want 
            'heat_source': 0.0,          # Energy of heat
            'neighbors': []               # List of adjacent points
        }

        set_temperature = self.attributes['temperature']
        set_material = self.attributes['material']

        self.quadrants = {
            Quadrant.Q1: False,
            Quadrant.Q2: False,
            Quadrant.Q3: False,
            Quadrant.Q4: False
        }
        


    def __str__(self):
        return f"Point({self.x}, {self.y})"