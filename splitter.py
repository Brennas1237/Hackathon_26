# This splits a geometric object into points and take a series of [x, y] coordinates and splits them into a list of points.
from Point import Point, PointType, Quadrant
import draw
from typing import List, Tuple, Dict, Optional, Set
import numpy as np


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

    def _establish_all_connections(self):
        """Create linked list connections between all grid points"""
        for (x, y), point in self.grid.items():

            right_coord = (x + self.resolution, y)
            if right_coord in self.grid:
                point.right = self.grid[right_coord]
                point.attributes['neighbors'].append(point.right)
            
            left_coord = (x - self.resolution, y)
            if left_coord in self.grid:
                point.left = self.grid[left_coord]
                point.attributes['neighbors'].append(point.left)
            
            down_coord = (x, y + self.resolution)
            if down_coord in self.grid:
                point.down = self.grid[down_coord]
                point.attributes['neighbors'].append(point.down)
            
            up_coord = (x, y - self.resolution)
            if up_coord in self.grid:
                point.up = self.grid[up_coord]
                point.attributes['neighbors'].append(point.up)
            
            # Quadrants (diagonals)
            q1_coord = (x + self.resolution, y - self.resolution)  # NE
            if q1_coord in self.grid:
                point.q1 = self.grid[q1_coord]
                point.quadrants[Quadrant.Q1] = True
            
            q2_coord = (x - self.resolution, y - self.resolution)  # NW
            if q2_coord in self.grid:
                point.q2 = self.grid[q2_coord]
                point.quadrants[Quadrant.Q2] = True
            
            q3_coord = (x - self.resolution, y + self.resolution)  # SW
            if q3_coord in self.grid:
                point.q3 = self.grid[q3_coord]
                point.quadrants[Quadrant.Q3] = True
            
            q4_coord = (x + self.resolution, y + self.resolution)  # SE
            if q4_coord in self.grid:
                point.q4 = self.grid[q4_coord]
                point.quadrants[Quadrant.Q4] = True

    def _classify_points_by_quadrants(self):
        """Classify points based on missing quadrants and maybe we can set rotation here too"""
        for point in self.drawn_points:
            # Check for root node
            if point.x == 0:
                point.attributes['type'] = PointType.ROOT
                point.attributes['rotation'] = 0
                point.attributes['root'] = True
                continue
            
            # Count missing quadrants among only drawn points
            # A quadrant is "missing" if the point in that quadrant is NOT drawn
            missing_count = 0
            for quadrant in Quadrant:
                quadrant_point = self._get_quadrant_point(point, quadrant)
                if not quadrant_point or not quadrant_point.is_drawn:
                    point.quadrants[quadrant] = False
                    missing_count += 1
                else:
                    point.quadrants[quadrant] = True
            
            # Classify based on missing quadrants
            # we need to know which quadrants are missing to determine rotation, so we will pass that info to the rotation function
            if missing_count == 0:
                # 0 missing quadrants: interior node
                point.attributes['type'] = PointType.INTERIOR
                point.attributes['rotation'] = self._calculate_rotation(point, missing_count ,[])
                
            elif missing_count == 1:
                # 1 missing quadrant: interior corner
                point.attributes['type'] = PointType.INTERIOR_CORNER
                missing = point.get_missing_quadrants()
                point.attributes['rotation'] = self._calculate_rotation(point, missing)
                
            elif missing_count == 2:
                # 2 missing quadrants: planar
                point.attributes['type'] = PointType.PLANAR
                missing = point.get_missing_quadrants()
                point.attributes['rotation'] = self._calculate_rotation(point, missing)
                
            elif missing_count == 3:
                # 3 missing quadrants: exterior corner
                point.attributes['type'] = PointType.EXTERIOR_CORNER
                missing = point.get_missing_quadrants()
                point.attributes['rotation'] = self._calculate_rotation(point, missing)

            else:
                # point should be deleted such that it will not be included in the final shape
                pass

    def _get_quadrant_point(self, point: Point, quadrant: Quadrant) -> Optional[Point]:
        """Get the point in the queried quadrant"""
        if quadrant == Quadrant.Q1:
            return point.q1
        elif quadrant == Quadrant.Q2:
            return point.q2
        elif quadrant == Quadrant.Q3:
            return point.q3
        elif quadrant == Quadrant.Q4:
            return point.q4
        return None    

    def _calculate_rotation(self, point: Point, missing_count, missing_quadrants: List[Quadrant]) -> int:
        """Calculate rotation based on which quadrants are missing"""

        def set_rotation(point):
            if missing_count == 0:
                rotation = 0
            elif missing_count == 1:
                rotation = (4 - missing_quadrants[0]) * np.pi / 2
            elif missing_count == 2:
                if missing_quadrants == ["Q1", "Q2"]:
                    rotation = 3 * np.pi / 2
                elif missing_quadrants == ["Q2", "Q3"]:
                    rotation = np.pi
                elif missing_quadrants == ["Q3", "Q4"]:
                    rotation = np.pi / 2
                elif missing_quadrants == ["Q1", "Q4"]:
                    rotation = 0
            elif missing_count == 3:
                if missing_quadrants == ["Q1", "Q2", "Q3"]:
                    rotation = 3 * np.pi / 2
                elif missing_quadrants == ["Q2", "Q3", "Q4"]:
                    rotation = np.pi
                elif missing_quadrants == ["Q1", "Q3", "Q4"]:
                    rotation = np.pi / 2
                elif missing_quadrants == ["Q1", "Q2", "Q4"]:
                    rotation = 0
            else:
                rotation = 0
        return rotation
        


