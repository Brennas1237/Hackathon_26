# Splitter plan
Purpose:
converts user drawn surface into a grid of points and assigns each of them a classification


Input: 
- it takes coordinates of a user drawn surface and splits them into points.
- 
Output:
- a linked list type where each point has: attributes


Functions:
- calculates length of surface (greatest value of surface)
- calculates number of x divisions (round int(length/delta_x))
- calculate number of points at each x division (round int(surface height at x / delta_x))
- make points into objects
- assign point attributes (classification, rotation)
  - if x coordinate = 0, root node, no rotation
  - if 0 missing quadrants: interior node, no rotation
  - if 1 missing quadrant: interior corner, rotate missing quadrant to q4
  - if 2 missing quadrants: planar, rotate missing quadrants to q1 and q4
  - if 3 missing quadrants: exterior corner, rotate missing quadrants to q1, q2,q4 