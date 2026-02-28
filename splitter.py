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
        
        # Classify all drawn points
        self._classify_points_by_quadrants()
        
        return drawn_points
    
    def shape_fill(self, shape_coordinates: List[Tuple[float, float]], material=None, temperature=20.0):
        """Given a list of shape coordinates (boundary), fill in the interior points
        
        Uses a scanline fill algorithm to find all interior points within the shape boundary.
        Assigns quadrant information and classifies all points as interior
        """
        print(f"Starting to fill shape")
        if len(shape_coordinates) < 3:
            print("Warning: Shape needs at least 3 points to fill")
            return self.add_drawn_shape(shape_coordinates, material, temperature)
        
        # First, add the boundary points
        boundary_points = self.add_drawn_shape(shape_coordinates, material, temperature)
        
        if not boundary_points:
            return []
        
        # Get all grid coordinates
        all_filled_points = set(boundary_points)
        
        # Find min and max bounds of the shape
        min_x = min(x for x, y in shape_coordinates)
        max_x = max(x for x, y in shape_coordinates)
        min_y = min(y for x, y in shape_coordinates)
        max_y = max(y for x, y in shape_coordinates)
        
        # Round to grid
        min_x = round(min_x / self.resolution) * self.resolution
        max_x = round(max_x / self.resolution) * self.resolution
        min_y = round(min_y / self.resolution) * self.resolution
        max_y = round(max_y / self.resolution) * self.resolution
        
        # Convert shape coordinates to grid points for polygon test
        grid_shape = []
        for x, y in shape_coordinates:
            grid_x = round(x / self.resolution) * self.resolution
            grid_y = round(y / self.resolution) * self.resolution
            grid_shape.append((grid_x, grid_y))
        
        # Scanline fill algorithm
        filled_points = []
        
        # For each row between min and max y
        y = min_y
        while y <= max_y:
            # Find intersections with shape boundary at this y
            intersections = []
            
            # Check each edge of the polygon
            for i in range(len(grid_shape)):
                p1 = grid_shape[i]
                p2 = grid_shape[(i + 1) % len(grid_shape)]
                
                # Skip horizontal edges
                if p1[1] == p2[1]:
                    continue
                
                # Check if this edge crosses our scanline
                if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                    # Calculate x intersection
                    x_intersect = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                    
                    # Round to grid
                    x_intersect = round(x_intersect / self.resolution) * self.resolution
                    intersections.append(x_intersect)
            
            # Sort intersections
            intersections.sort()
            
            # Fill between pairs of intersections
            for i in range(0, len(intersections), 2):
                if i + 1 < len(intersections):
                    x_start = intersections[i]
                    x_end = intersections[i + 1]
                    
                    # Fill all grid points between x_start and x_end
                    x = x_start
                    while x <= x_end:
                        if (x, y) in self.grid:
                            point = self.grid[(x, y)]
                            
                            # Only fill if not already drawn
                            if not point.is_drawn:
                                point.is_drawn = True
                                point.attributes['material'] = material
                                point.attributes['temperature'] = temperature
                                point.attributes['type'] = PointType.INTERIOR
                                point.attributes['rotation'] = 0.0
                                self.drawn_points.add(point)
                                filled_points.append(point)
                                all_filled_points.add(point)
                        
                        x += self.resolution
            
            y += self.resolution
        
        # Reclassify all points (including new interior ones)
        self._classify_points_by_quadrants()
        
        print(f"Shape fill complete: {len(boundary_points)} boundary points, {len(filled_points)} interior points")
        return list(all_filled_points)

    def _classify_points_by_quadrants(self):
        """Classify points based on missing quadrants and set rotation"""
        for point in self.drawn_points:
            # Check for root node
            if point.x == 0:
                point.attributes['type'] = PointType.ROOT
                point.attributes['rotation'] = 0.0
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
                    print(f"Point at ({point.x}, {point.y}) is missing Q4, Q2, Q1 - rotation set to π/2 or {rotation}")
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
        # with a print to help us know what is going wrong
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
        
        print(f"Total points filled in: {len(self.all_points)}")

        print("\n" + "="*60)


    def get_temperature_field(self) -> List[List[float]]:
        """Get 2D array of temperatures for visualization, this will be useful later for color mapping"""
        cols = int(self.width / self.resolution)
        rows = int(self.height / self.resolution)
        
        field = [[20.0 for j in range(cols)] for j in range(rows)]
        
        for (x, y), point in self.grid.items():
            if point.is_drawn:
                col = int(x / self.resolution)
                row = int(y / self.resolution)
                field[row][col] = point.attributes['temperature']
                
        return field
    
    def get_points_by_type(self, point_type: PointType) -> List[Point]:
        """Get all points of a specific type"""
        return [p for p in self.drawn_points if p.attributes.get('type') == point_type]
    
    def get_point_at(self, x: float, y: float) -> Optional[Point]:
        """Get point at specific grid coordinates"""
        x = round(x / self.resolution) * self.resolution
        y = round(y / self.resolution) * self.resolution
        return self.grid.get((x, y))
    
    def clear_shape(self):
        """Clear all drawn points
        if we want to reset the drawing we can just call this"""
        for point in self.drawn_points:
            point.is_drawn = False
            point.attributes['type'] = None
            point.attributes['material'] = None
            point.attributes['temperature'] = 20.0
            point.attributes['root'] = False
        
        self.drawn_points.clear()
        print("Shape cleared")