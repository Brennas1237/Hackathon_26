import sympy as sp
import numpy as np
def set_equations(point_list, T_base, T_free_stream, h, delta_x, k):
    """
    Generate equations for each point considering neighbors, rotation, 
    and boundary conditions, avoiding singular matrices.
    """
    valid_points = {(p.x, p.y) for p in point_list}

    for point in point_list:
        n, m = point.x, point.y
        rot = point.attributes['rotation']
        missing_count = point.count_missing_quadrants()

        # Symbols
        T = sp.Symbol(f'T_{n}_{m}')

        # Compute neighbor coordinates based on rotation
        neighbors = [
            (n + int(np.cos(rot)), m + int(np.sin(rot))),  # T1
            (n - int(np.sin(rot)), m + int(np.cos(rot))),  # T2
            (n - int(np.cos(rot)), m - int(np.sin(rot))),  # T3
            (n + int(np.sin(rot)), m - int(np.cos(rot)))   # T4
        ]

        lhs_terms = []
        rhs = 0

        # Loop over neighbors
        for nx, ny in neighbors:
            if (nx, ny) in valid_points:
                lhs_terms.append(sp.Symbol(f'T_{nx}_{ny}'))
            else:
                # Missing neighbor → move contribution to RHS
                rhs += 2 * (h * delta_x / k) * T_free_stream

        # Build equation depending on missing count and location
        if n == 0:  # Left boundary: Dirichlet
            eq = sp.Eq(T, T_base)
        else:
            # Sum of neighbors on LHS minus coefficient*central T
            coeff = 2 * (len(lhs_terms) + h * delta_x / k)
            eq = sp.Eq(sum(lhs_terms), coeff * T - rhs)

        # Store equation and symbol
        point.attributes['equation'] = eq
        point.attributes['label'] = T


def make_equation_list(point_list):
    equation_list = []
    for point in point_list:
        equation = point.attributes['equation']
        equation_list.append(equation)
    return equation_list

def make_variable_list(point_list):
    variable_list = []
    for point in point_list:
        variable = point.attributes['label']
        variable_list.append(variable)
    return variable_list

def solve_system(equation_list, variable_list):
    try:
        # Convert to matrix form
        coefficient_matrix, solution_vector = sp.linear_eq_to_matrix(equation_list, variable_list)
        
        # Convert to numpy arrays with proper type handling
        coefficient_matrix = np.array(coefficient_matrix).astype(np.float64)
        solution_vector = np.array(solution_vector).astype(np.float64).flatten()
        
        # Solve the linear system
        temperature_list = np.linalg.solve(coefficient_matrix, solution_vector)
        return temperature_list
    except Exception as e:
        print(f"Error solving system: {e}")
        print(f"Equations: {equation_list}")
        print(f"Variables: {variable_list}")
        raise

def assign_temp_to_point(point_list, temperature_list):
    for p, t in zip(point_list, temperature_list):
        p.attributes['temperature'] = float(t)  # Ensure conversion to float