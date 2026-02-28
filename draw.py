class Draw:
    def __init__(self, System):
        # allows a user to draw a shape by clicking and dragging the mouse. The shape is defined by a series of points that are collected as the user drags the mouse. The class also includes methods to check if the shape is touching the walls of the drawing area, and to close the shape if it is not touching the walls.
        self.shape = []
        self.material = None # a material from a dictionary of materials in materials.py
        self.temp = None # int
        self.system = System

    def start_draw(self, origin):
        self.shape.append(origin)
    
    def continue_draw(self, point):
        self.shape.append(point)
    
    def end_draw(self):
        if not self.is_touching_wall():
            self.close_shape()
        self.construct_shape()

    def user_input(self, input):
        # Placeholder for user input handling logic
        
        if input == "start":
            if input != (0, 0): # Assuming (0, 0) is the origin
                # send a message that the user must start drawing from the origin
                pass
            else:
                self.start_draw(input)
                if input == "continue":
                    self.continue_draw(input)
                else:
                    self.end_draw()
        pass

    def is_touching_wall(self):
        if self.shape:
            for point in self.shape:
                if point[0] <= 0 or point[0] >= self.system.get_width() or point[1] <= 0 or point[1] >= self.system.get_height():
                    return True
        return False
    
    def close_shape(self):
        """This does not close to the first point. Instead it adds all of the points needed to touch the y axis"""
        if self.shape:
            last_point = self.shape[-1]
            # If the last point is not on the y-axis, add points to touch it
            if last_point[1] != 0:
                # Add points to reach y=0
                for y in range(last_point[1], 0, -1):
                    self.shape.append((last_point[0], y))
    
    def construct_shape(self):
        # Placeholder for shape construction logic
        # This would involve integrating the points to create a data structure representing the shape, and applying the material properties.
        constructed_shape = []
        for point in self.shape:
            constructed_shape.append(point)
        return constructed_shape







