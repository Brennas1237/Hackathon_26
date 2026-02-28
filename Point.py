from typing import Optional
from Enum import PointType, Quadrant
import sympy as sp

class Point:
    def __init__(self, x: float, y: float, temperature: float = 20.0, material: Optional[str] = None):
        self.x = x
        self.y = y
        self.coordinates = (x, y)
        self.is_drawn = False
        
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

        self.quadrants = {
            Quadrant.Q1: False,
            Quadrant.Q2: False,
            Quadrant.Q3: False,
            Quadrant.Q4: False
        }

         # Point attributes as a dictionary
        self.attributes = {
            'type': None,           # PointType (exterior, interior, planar, root, corner)
            'root': False,          
            'temperature': 20.0,     # Current temperature
            'material': None,        # Material at this point
            'heat_source': 0.0,          # Energy of heat
            'neighbors': [] ,              # List of adjacent points
            'rotation': 0.0,
            'equation': None,
            "label": None
        }

        set_temperature = self.attributes['temperature']
        set_material = self.attributes['material']

        self.quadrants = {
            Quadrant.Q1: False,
            Quadrant.Q2: False,
            Quadrant.Q3: False,
            Quadrant.Q4: False
        }

    def get_missing_quadrants(self):
        """Return a list of missing quadrants for this point"""
        missing = []
        for quadrant, has_point in self.quadrants.items():
            if not has_point:
                missing.append(quadrant)
        return missing

    def count_missing_quadrants(self) -> int:
        """Count how many quadrants are missing (have no point)"""
        return sum(1 for present in self.quadrants.values() if not present)
        
    def __str__(self):
        return f"Point({self.x}, {self.y})"