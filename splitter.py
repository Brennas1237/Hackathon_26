# This splits a geometric object into points and take a series of [x, y] coordinates and splits them into a list of points.
from typing import List, Tuple, Dict, Optional, Set
import numpy as np
from Point import Point
from Enum import PointType, Quadrant

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

    def _initialize_grid(self):
        """Initialize entire grid as exterior points"""
        cols = int(self.width / self.resolution)
        rows = int(self.height / self.resolution)
        
        for row in range(rows):
            for col in range(cols):
                x = col * self.resolution
                y = row * self.resolution
                self.grid[(x, y)] = Point(x, y)
        
        # Establish all connections
        self._establish_all_connections()

    def _establish_all_connections(self):
        """Create linked list connections between all grid points"""
        for (x, y), point in self.grid.items():
            # Clear neighbors list first
            point.attributes['neighbors'] = []
            
            # Reset quadrants
            for q in Quadrant:
                point.quadrants[q] = False

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

    def add_drawn_shape(self, coordinates: List[Tuple[float, float]], material=None, temperature=20.0):
        """Add a drawn shape to the grid"""
        drawn_points = []
        
        for coord in coordinates:
            x, y = coord
            # Round to grid
            x = round(x / self.resolution) * self.resolution
            y = round(y / self.resolution) * self.resolution
            
            if (x, y) in self.grid:
                point = self.grid[(x, y)]
                
                if not point.is_drawn:
                    point.is_drawn = True
                    point.attributes['material'] = material
                    point.attributes['temperature'] = temperature
                    self.drawn_points.add(point)
                    drawn_points.append(point)
        
        # Classify all drawn points
        self._classify_points_by_quadrants()
        
        return drawn_points

    def _classify_points_by_quadrants(self):
        """Classify points based on missing quadrants and set rotation"""
        for point in self.drawn_points:
            # Check for root node
            if point.x == 0:
                point.attributes['type'] = PointType.ROOT
                point.attributes['rotation'] = 0
                point.attributes['root'] = True
                continue
            
            # First, update quadrants based on drawn status of diagonal neighbors
            self._update_point_quadrants(point)
            
            # Count missing quadrants among drawn points
            missing_count = point.count_missing_quadrants()
            missing_quadrants = point.get_missing_quadrants()
            
            # Classify based on missing quadrants
            if missing_count == 0:
                # 0 missing quadrants: interior node
                point.attributes['type'] = PointType.INTERIOR
                point.attributes['rotation'] = self._calculate_rotation(point, missing_count, missing_quadrants)
                
            elif missing_count == 1:
                # 1 missing quadrant: interior corner
                point.attributes['type'] = PointType.INTERIOR_CORNER
                point.attributes['rotation'] = self._calculate_rotation(point, missing_count, missing_quadrants)
                
            elif missing_count == 2:
                # 2 missing quadrants: planar
                point.attributes['type'] = PointType.PLANAR
                point.attributes['rotation'] = self._calculate_rotation(point, missing_count, missing_quadrants)
                
            elif missing_count == 3:
                # 3 missing quadrants: exterior corner
                point.attributes['type'] = PointType.EXTERIOR_CORNER
                point.attributes['rotation'] = self._calculate_rotation(point, missing_count, missing_quadrants)
            else:
                # 4 missing quadrants - isolated point, should be exterior
                point.attributes['type'] = PointType.EXTERIOR
                point.attributes['rotation'] = 0

    def _update_point_quadrants(self, point: Point):
        """Update quadrant booleans based on whether diagonal points are drawn"""
        # Check each diagonal neighbor
        if point.q1 and point.q1.is_drawn:
            point.quadrants[Quadrant.Q1] = True
        else:
            point.quadrants[Quadrant.Q1] = False
            
        if point.q2 and point.q2.is_drawn:
            point.quadrants[Quadrant.Q2] = True
        else:
            point.quadrants[Quadrant.Q2] = False
            
        if point.q3 and point.q3.is_drawn:
            point.quadrants[Quadrant.Q3] = True
        else:
            point.quadrants[Quadrant.Q3] = False
            
        if point.q4 and point.q4.is_drawn:
            point.quadrants[Quadrant.Q4] = True
        else:
            point.quadrants[Quadrant.Q4] = False

    def _get_quadrant_point(self, point: Point, quadrant: Quadrant):
        """Get the point in the queried quadrant
        Return optional """
        if quadrant == Quadrant.Q1:
            return point.q1
        elif quadrant == Quadrant.Q2:
            return point.q2
        elif quadrant == Quadrant.Q3:
            return point.q3
        elif quadrant == Quadrant.Q4:
            return point.q4
        return None    

    def _calculate_rotation(self, point: Point, missing_count: int, missing_quadrants: List[Quadrant]):
        """Calculate rotation in radians based on which quadrants are missing"""
        # Convert Quadrant enums to strings for comparison
        missing_str = [q.value for q in missing_quadrants]
        
        if missing_count == 0:
            rotation = 0.0
        elif missing_count == 1:
            # Map quadrant to rotation (rotate missing to Q4)
            # Q4 missing -> 0, Q3 missing -> π/2, Q2 missing -> π, Q1 missing -> 3π/2
            if missing_quadrants[0] == Quadrant.Q4:
                rotation = 0.0
            elif missing_quadrants[0] == Quadrant.Q3:
                rotation = np.pi/2
            elif missing_quadrants[0] == Quadrant.Q2:
                rotation = np.pi
            elif missing_quadrants[0] == Quadrant.Q1:
                rotation = 3*np.pi/2
            else:
                rotation = 0.0
        elif missing_count == 2:
            if set(missing_str) == {"q1", "q2"}:
                rotation = 3 * np.pi / 2
            elif set(missing_str) == {"q2", "q3"}:
                rotation = np.pi
            elif set(missing_str) == {"q3", "q4"}:
                rotation = np.pi / 2
            elif set(missing_str) == {"q1", "q4"}:
                rotation = 0.0
            else:
                rotation = 0.0
        elif missing_count == 3:
            # Find which quadrant IS present
            present = [q for q in Quadrant if q not in missing_quadrants]
            if present:
                if present[0] == Quadrant.Q4:
                    rotation = 0.0
                elif present[0] == Quadrant.Q3:
                    rotation = np.pi/2
                elif present[0] == Quadrant.Q2:
                    rotation = np.pi
                elif present[0] == Quadrant.Q1:
                    rotation = 3*np.pi/2
                else:
                    rotation = 0.0
            else:
                rotation = 0.0
        else:
            rotation = 0.0
        
        # Store rotation in degrees as well for easier use
        point.attributes['rotation_deg'] = rotation * 180 / np.pi
        return rotation
    


