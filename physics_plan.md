# Physics Plan
Purpose:
build the equation to calculate the temperature of each node

Input:
- point type and missing quadrants

Output:
- temperature equation

Functions:
- calculate rotation value based on missing quadrant
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
  
- for point (n,m) equations are
  - if root node
    - T(n,m) = Base Temperature
  - if interior node
    - T(n, m+1) + T(n,m-1) + T(n+1,m) + T(n-1,m) - 4 * T(n,m)
  - if interior corner
    - 2(T(n-cos(rot),m) + T(n, m+sin(rot))) + T(n+cos(rot),m) + T(n,m-sin(rot)) - 2(3+h*delta_x/k)T(n,m) = -2(h*delta_x/k)T_free_stream
  - if planar 
    - 2(T(n-cos(rot),m) + T(n,m+sin(rot)) + T(n,m-sin(rot))) - 2(h*delta_x/k + 2)T(n,m) = -2h * delta_x /k * T_free_stream
  - if exterior corner
    - T(n,m-sin(rot)) + T(n-cos(rot),m) -2(h*delta_x/k + 2)T(n,m) = -2h*delta_x/k * T_free_stream
