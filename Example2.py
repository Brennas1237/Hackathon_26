import sympy as sp
import numpy as np


# 1. Define variables
x, y, z = sp.symbols('x, y, z')

# 2. Define the equations (must be expressions equal to zero or use sympy.Eq)
# It is best practice to rewrite equations to equal zero first.
eq1 = x + y + z - 1
eq2 = x + y + 2*z - 3
eq3 = x - y + 3*z - 4

equations = [eq1, eq2, eq3]
variables = [x, y, z]

# 3. Convert to matrix form
A, b = sp.linear_eq_to_matrix(equations, variables)

A = sp.matrix2numpy(A, dtype=float)
b = sp.matrix2numpy(b, dtype=float)
print(np.linalg.solve(A, b))