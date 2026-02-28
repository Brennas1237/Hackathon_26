import Point
from typing import List, Tuple

class Draw:
    def __init__(self, system):
        self.shape_coords: List[Tuple[float, float]] = []  
        self.material = None
        self.temp = 20.0
        self.system = system  # Store reference to the system
        
    def start_draw(self, origin: Tuple[float, float]):
        """Start drawing at origin"""
        self.shape_coords = [origin]
        
    def continue_draw(self, point: Tuple[float, float]):
        """Add point to shape"""
        self.shape_coords.append(point)
        
    def end_draw(self):
        """Finish drawing and add to system"""
        if not self.is_touching_wall():
            self.close_shape()
        
        # Add shape to system's data structure
        # The system object has the add_drawn_shape method
        self.system.add_drawn_shape(
            self.shape_coords,
            material=self.material,
            temperature=self.temp
        )
        
    def is_touching_wall(self) -> bool:
        """Check if shape touches wall"""
        if not self.shape_coords:
            return False
        
        for x, y in self.shape_coords:
            if x <= 0 or x >= self.system.width or y <= 0 or y >= self.system.height:
                return True
        return False
    
    def close_shape(self):
        """Close shape to y-axis"""
        if self.shape_coords:
            last_x, last_y = self.shape_coords[-1]
            if last_y != 0:
                steps = int(abs(last_y) / self.system.resolution)
                for i in range(1, steps + 1):
                    new_y = last_y - i * self.system.resolution
                    self.shape_coords.append((last_x, new_y))
    
    def set_material(self, material):
        self.material = material
        
    def set_temperature(self, temp):
        self.temp = temp