# Math Plan
Purpose: calculate the temperature at each node

Input:
- List of sympy equations
- List of sympy varialbles

Output:
- List of temperatures for each point

Function:
- imports list of equations from physics
- imports list of variables from physics
- use "A, b = sp.linear_eq_to_matrix(equations, variables)" to convert into coefficient matrix and solution vector
- use "A = sp.matrix2numpy(A, dtype=float)" to convert A to a numpy array 
- use "b = sp.matrix2numpy(b, dtype=float)" to convert B to a numpy array
- use "temperature_list = np.linalg.solve(A,b)" to solve for all temperatures
- 