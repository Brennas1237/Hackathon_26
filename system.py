class System:
    """A class to represent the window in which the drawing takes place.
      It holds the dimensions of the drawing area and can be used to check for boundaries when drawing shapes."""
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def set_width(self, width):
        self.width = width
    def set_height(self, height):
        self.height = height