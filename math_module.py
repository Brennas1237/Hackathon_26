import sympy as sp
import numpy as np
from Enum import PointType

def set_equations(point_list, T_base, T_free_stream, h, delta_x, k):
    valid_points = {(p.x, p.y) for p in point_list}

    for point in point_list:
        n, m = point.x, point.y
        T = sp.Symbol(f'T{n}x{m}')
        rot = point.attributes.get('rotation', 0)
        
        # Get the point type enum directly
        point_type = point.attributes.get('type')
        
        # Calculate rotated coordinates
        cos_rot = int(np.cos(rot))
        sin_rot = int(np.sin(rot))
        
        # Check if this is a root node (x=0 overrides other types)
        if n == 0:
            # Root node
            eq = T - T_base
            print(f"Point({n},{m}) ROOT (x=0): T = {T_base}")
            
        # Otherwise use the point type
        elif point_type == PointType.INTERIOR:
            # Interior node
            T_up    = sp.Symbol(f'T{n}x{m+1}') if (n, m+1) in valid_points else 0
            T_down  = sp.Symbol(f'T{n}x{m-1}') if (n, m-1) in valid_points else 0
            T_right = sp.Symbol(f'T{n+1}x{m}') if (n+1, m) in valid_points else 0
            T_left  = sp.Symbol(f'T{n-1}x{m}') if (n-1, m) in valid_points else 0
            eq = T_up + T_down + T_right + T_left - 4*T
            print(f"Point({n},{m}) INTERIOR: conduction only")
            
        elif point_type == PointType.INTERIOR_CORNER:
            # Interior corner
            T_nc_m = sp.Symbol(f'T{n - cos_rot}x{m}') if (n - cos_rot, m) in valid_points else 0
            T_n_ms = sp.Symbol(f'T{n}x{m + sin_rot}') if (n, m + sin_rot) in valid_points else 0
            T_nc2_m = sp.Symbol(f'T{n + cos_rot}x{m}') if (n + cos_rot, m) in valid_points else 0
            T_n_ms2 = sp.Symbol(f'T{n}x{m - sin_rot}') if (n, m - sin_rot) in valid_points else 0
            
            eq = (2*(T_nc_m + T_n_ms) + T_nc2_m + T_n_ms2 
                  - 2*(3 + h*delta_x/k)*T 
                  + 2*(h*delta_x/k)*T_free_stream)
            print(f"Point({n},{m}) INTERIOR_CORNER")
            
        elif point_type == PointType.PLANAR:
            # Planar surface
            T_nc_m = sp.Symbol(f'T{n - cos_rot}x{m}') if (n - cos_rot, m) in valid_points else 0
            T_n_ms = sp.Symbol(f'T{n}x{m + sin_rot}') if (n, m + sin_rot) in valid_points else 0
            T_n_ms2 = sp.Symbol(f'T{n}x{m - sin_rot}') if (n, m - sin_rot) in valid_points else 0
            
            eq = (2*(T_nc_m + T_n_ms + T_n_ms2) 
                  - 2*(2 + h*delta_x/k)*T 
                  + 2*(h*delta_x/k)*T_free_stream)
            print(f"Point({n},{m}) PLANAR")
            
        elif point_type == PointType.EXTERIOR_CORNER:
            # Exterior corner
            T_n_ms = sp.Symbol(f'T{n}x{m - sin_rot}') if (n, m - sin_rot) in valid_points else 0
            T_nc_m = sp.Symbol(f'T{n - cos_rot}x{m}') if (n - cos_rot, m) in valid_points else 0
            
            eq = (T_n_ms + T_nc_m 
                  - 2*(2 + h*delta_x/k)*T 
                  + 2*(h*delta_x/k)*T_free_stream)
            print(f"Point({n},{m}) EXTERIOR_CORNER")
            
        elif point_type == PointType.ROOT and n != 0:
            # Root but not at x=0 (unlikely, but handle it)
            eq = T - T_base
            print(f"Point({n},{m}) ROOT (non-zero x)")
            
        else:
            # Fallback - this should not happen if types are set correctly
            print(f"WARNING: Point({n},{m}) has type {point_type}, using interior fallback")
            T_up    = sp.Symbol(f'T{n}x{m+1}') if (n, m+1) in valid_points else 0
            T_down  = sp.Symbol(f'T{n}x{m-1}') if (n, m-1) in valid_points else 0
            T_right = sp.Symbol(f'T{n+1}x{m}') if (n+1, m) in valid_points else 0
            T_left  = sp.Symbol(f'T{n-1}x{m}') if (n-1, m) in valid_points else 0
            eq = T_up + T_down + T_right + T_left - 4*T

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
    max_temp = np.max(temperature_list)
    
    for p, t in zip(point_list, temperature_list):
        # add max temp divided by distance
        p.attributes['temperature'] = float(t)