from splitter import ShapeDataStructure

if __name__ == "__main__":
    from draw import Draw
    
    # Initialize drawing system and get user input for shape drawing

    # draw = Draw()
    # # get user input for shape drawing
    
    # splitter = Splitter(width=2, height=2, resolution=1)
    # splitter.split_shape(draw.shape)

    system = ShapeDataStructure(width=20, height=20, resolution=1.0)
    
    # Draw a plus sign shape to test different point types
    shape_coords = []
    
    # Horizontal line
    for x in range(0, 21):
        shape_coords.append((x, 1))
    
    # Vertical line
    # for y in range(5, 16):
    #     if y != 10:  # Skip center (already added)
    #         shape_coords.append((10, y))
    
    # Add the shape
    system.integrate_under_line(shape_coords, material="copper", temperature=100.0)
    
    # Print classification
    system.print_classification()