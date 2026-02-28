class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.attributes = {}

    def __str__(self):
        return f"Point({self.x}, {self.y})"