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
        self.all_points: Set[Point] = set(self.grid.values())

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

            # Cardinal directions (4-directional)
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
        print("Establishing drawn shape on grid")
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

        self._classify_points_by_quadrants()

        return drawn_points
    
    def integrate_under_line(self, coordinates, k_value=None, h_value=None, temperature=20.0):
        """
        Fill all grid points vertically under a drawn line.
        Stores numeric thermal properties for physics simulation.
        """
        print("Integrating under drawn line")

        # First add the boundary points
        boundary_points = self.add_drawn_shape(coordinates, material=None, temperature=temperature)

        if not boundary_points:
            return []

        # Group boundary points by x coordinate
        column_heights = {}
        for point in boundary_points:
            x = point.x
            y = point.y
            if x not in column_heights:
                column_heights[x] = y
            else:
                column_heights[x] = max(column_heights[x], y)

        filled_points = []

        # Fill each column from y=0 to max_y
        for x, max_y in column_heights.items():
            y = 0
            while y <= max_y:
                if (x, y) in self.grid:
                    point = self.grid[(x, y)]
                    if not point.is_drawn:
                        point.is_drawn = True
                        # Store numeric thermal properties
                        point.attributes['k'] = k_value
                        point.attributes['h'] = h_value
                        point.attributes['temperature'] = temperature
                        self.drawn_points.add(point)
                        filled_points.append(point)
                y += self.resolution

        print(f"Integrated {len(filled_points)} interior points with k={k_value}, h={h_value}")
        
        self._classify_points_by_quadrants()
        for i, point in enumerate(list(self.shape.drawn_points)[:10]):
            print(f"Point {i}: ({point.x},{point.y}) type={point.attributes['type']}")
        return filled_points

    def _classify_points_by_quadrants(self):
        """Classify points based on missing quadrants and set rotation"""
        # First reset all quadrants for drawn points
        for point in self.drawn_points:
            for q in Quadrant:
                point.quadrants[q] = False
    
        # Then update quadrants based on actual diagonal connections
        for point in self.drawn_points:
            # Check each diagonal neighbor and set quadrant if it exists AND is drawn
            if point.q1 is not None:
                point.quadrants[Quadrant.Q1] = point.q1.is_drawn
            if point.q2 is not None:
                point.quadrants[Quadrant.Q2] = point.q2.is_drawn
            if point.q3 is not None:
                point.quadrants[Quadrant.Q3] = point.q3.is_drawn
            if point.q4 is not None:
                point.quadrants[Quadrant.Q4] = point.q4.is_drawn
        
        # Now classify based on updated quadrants
        for point in self.drawn_points:
            # Check for root node (heat source at x=0)
            if point.x == 0:
                point.attributes['type'] = PointType.ROOT
                point.attributes['rotation'] = 0.0
                point.attributes['root'] = True
                continue
            
            # Count missing quadrants
            missing_count = point.count_missing_quadrants()
            missing_quadrants = point.get_missing_quadrants()
            
            # Classify based on missing quadrants
            if missing_count == 0:
                point.attributes['type'] = PointType.INTERIOR
            elif missing_count == 1:
                point.attributes['type'] = PointType.INTERIOR_CORNER
            elif missing_count == 2:
                point.attributes['type'] = PointType.PLANAR
            elif missing_count == 3:
                point.attributes['type'] = PointType.EXTERIOR_CORNER
            else: # missing_count == 4:
                point.attributes['type'] = PointType.PLANAR
            
            # Calculate rotation
            point.attributes['rotation'] = self._calculate_rotation(point, missing_count, missing_quadrants)

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
        
        return rotation

    def update_neighbors(self, point: Point):
        """Update the neighbors list for a point based on the new rotation"""
        rotation = point.attributes.get('rotation', 0)
        if rotation == 0:
            pass
    
    def print_classification(self):
        """Utility function to print classification of all drawn points by type"""
        if not self.drawn_points:
            print("No drawn points to classify")
            return
        
        # Group points by type
        points_by_type = {}
        for point_type in PointType:
            points_by_type[point_type] = []
        
        for point in self.drawn_points:
            point_type = point.attributes.get('type')
            if point_type in points_by_type:
                points_by_type[point_type].append(point)
        
        # Print summary
        print("\n" + "="*60)
        print("POINT CLASSIFICATION SUMMARY")
        print("="*60)
        
        total_points = len(self.drawn_points)
        print(f"Total drawn points: {total_points}")
        
        for point_type, points in points_by_type.items():
            if points:
                count = len(points)
                percentage = (count / total_points) * 100
                print(f"\n{point_type.value.upper()}: {count} points ({percentage:.1f}%)")
                
                # Show sample points (up to 5)
                for i, point in enumerate(points[:5]):
                    missing = point.get_missing_quadrants()
                    missing_str = [q.value for q in missing] if missing else ["none"]
                    rotation = point.attributes.get('rotation', 0)
                    print(f"  {i+1}. ({point.x}, {point.y}) - Missing: {missing_str}, Rot: {rotation:.2f} radians")
                
                if len(points) > 5:
                    print(f"     ... and {len(points) - 5} more")
        
        print(f"Total points filled in: {len(self.drawn_points)}")
        print("\n" + "="*60)

    def get_points_by_type(self, point_type: PointType) -> List[Point]:
        """Get all points of a specific type"""
        return [p for p in self.drawn_points if p.attributes.get('type') == point_type]
    
    def get_point_at(self, x: float, y: float) -> Optional[Point]:
        """Get point at specific grid coordinates"""
        x = round(x / self.resolution) * self.resolution
        y = round(y / self.resolution) * self.resolution
        return self.grid.get((x, y))
    
    def clear_shape(self):
        """Clear all drawn points"""
        for point in self.drawn_points:
            point.is_drawn = False
            point.attributes['type'] = None
            point.attributes['material'] = None
            point.attributes['temperature'] = 20.0
            point.attributes['root'] = False
            point.attributes['k'] = None
            point.attributes['h'] = None
        
        self.drawn_points.clear()
        print("Shape cleared")