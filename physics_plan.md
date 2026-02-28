# Physics Plan
Purpose:
build the equation to calculate the temperature of each node

Input:
- point type and missing quadrants

Output:
- sympy equation for temperature at node

Functions: 
- for point (n,m) equations are
  - if root node
    - T(n,m) = Base Temperature
  - if interior node
    - T(n, m+1) + T(n,m-1) + T(n+1,m) + T(n-1,m) - 4 * T(n,m) = 0
  - if interior corner
    - 2(T(n-cos(rot),m) + T(n, m+sin(rot))) + T(n+cos(rot),m) + T(n,m-sin(rot)) - 2(3+h*delta_x/k)T(n,m) + 2(h*delta_x/k)T_free_stream = 0
  - if planar 
    - 2(T(n-cos(rot),m) + T(n,m+sin(rot)) + T(n,m-sin(rot))) - 2(h*delta_x/k + 2)T(n,m) + 2h * delta_x /k * T_free_stream = 0
  - if exterior corner
    - T(n,m-sin(rot)) + T(n-cos(rot),m) -2(h*delta_x/k + 2)T(n,m) + 2h*delta_x/k * T_free_stream = 0
