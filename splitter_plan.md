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
- assign point attributes (classification, rotation)
  - if x coordinate = 0, root node, no rotation
  - if 0 missing quadrants: interior node, no rotation
  - if 1 missing quadrant: interior corner, rotate missing quadrant to q4
  - if 2 missing quadrants: planar, rotate missing quadrants to q1 and q4
  - if 3 missing quadrants: exterior corner, rotate missing quadrants to q1, q2,q4 

Calculate rotation value based on missing quadrant
  Gets passed in a list of missing quadrants, the number of missing quadrants, and the point to adjust the attribute
  - if root node -> rotation = 0
  - if interior node -> rotation = 0
  - if interior corner -> rotation = (4 - missing quadrant #) * pi/2
  - if planar -> 
    - if q1 & q2 missing -> rotation = 3pi/2
    - if q2 & q3 missing -> rotation = pi
    - if q3 & q4 missing -> rotation = pi/2
    - if q1 & q4 missing - rotation = 0
  - if exterior corner -> 
    - if q1 & q2 & q3 missing -> rotation = 3pi/2
    - if q2 & q3 & q4 missing -> rotation = pi
    - if q3 & q4 & q1 missing -> rotation = pi/2
    - if q4 & q1 & q2 missing -> rotation = 0

