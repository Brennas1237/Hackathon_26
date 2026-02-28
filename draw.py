from splitter import ShapeDataStructure
import Point

class Draw:
    def __init__(self, system):
        self.shape = []  # List of Point objects
        self.material = None
        self.temp = None
        self.system = system
        self.origin_coords = (0, 0)
        self.shape_data = ShapeDataStructure()
        
    def start_draw(self, origin):
        """Start drawing at origin"""
        point = Point(origin[0], origin[1])
        self.shape.append(point)
        
    def continue_draw(self, point_coords):
        """Add point to shape"""
        point = Point(point_coords[0], point_coords[1])
        self.shape.append(point)
        
    def end_draw(self):
        """Finish drawing and construct shape"""
        if not self.is_touching_wall():
            self.close_shape()
        
        # Convert shape points to coordinates and set up point attributes
        coords = [(p.x, p.y) for p in self.shape]
        points = self.shape_data.set_up_points(coords)
        
        # Apply material and temperature to all points
        for point in points:
            point.attributes['material'] = self.material
            point.attributes['temperature'] = self.temp
            if self.material:
                pass # Set material-specific attributes if needed
        
        self.construct_shape()
        
    def close_shape(self):
        """Close shape to y-axis if not touching wall"""
        if self.shape:
            # last item in shape is the last point drawn
            last_point = self.shape[-1]
            # if not touching wall, add points to close shape to y-axis
            if last_point.y != 0:
                # Add points to reach y=0
                steps = int(abs(last_point.y) / self.system.get_resolution())
                for i in range(1, steps + 1):
                    new_y = last_point.y - i * self.system.get_resolution()
                    self.shape.append(Point(last_point.x, new_y))
    
    def set_material(self, material):
        self.material = material
    def get_material(self):
        return self.material
    def set_temp(self, temp):
        self.temp = temp
    def get_temp(self):
        return self.temp
    def set_origin_coords(self, x, y):
        self.origin_coords = (x, y)
    def get_origin_coords(self):
        return self.origin_coords







