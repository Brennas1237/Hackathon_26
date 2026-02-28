
from enum import Enum
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
