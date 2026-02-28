import sympy as sp
import numpy as np


def set_equations(point_list, T_base, T_free_stream, h, delta_x, k):
    valid_points = {(p.x, p.y) for p in point_list}

    for point in point_list:
        n, m = point.x, point.y
        T = sp.Symbol(f'T{n}{m}')
        rot = point.attributes.get('rotation', 0)
        point_type = point.attributes.get('type', 'interior')
        is_source = point.attributes.get('is_source', False)

        if is_source:
            # Heat source: just fix the temperature
            eq = T - point.attributes['T_source']
        elif point_type == 'root':
            eq = T - T_base
        elif point_type == 'interior':
            T_up    = sp.Symbol(f'T{n}{m+1}') if (n, m+1) in valid_points else T_free_stream
            T_down  = sp.Symbol(f'T{n}{m-1}') if (n, m-1) in valid_points else T_free_stream
            T_right = sp.Symbol(f'T{n+1}{m}') if (n+1, m) in valid_points else T_free_stream
            T_left  = sp.Symbol(f'T{n-1}{m}') if (n-1, m) in valid_points else T_free_stream
            eq = T_up + T_down + T_right + T_left - 4*T
        elif point_type == 'interior_corner':
            T1 = 2 * (sp.Symbol(f'T{int(n - np.cos(rot))}{int(m)}') if (int(n - np.cos(rot)), m) in valid_points else T_free_stream)
            T2 = 2 * (sp.Symbol(f'T{n}{int(m + np.sin(rot))}') if (n, int(m + np.sin(rot))) in valid_points else T_free_stream)
            T3 = sp.Symbol(f'T{int(n + np.cos(rot))}{m}') if (int(n + np.cos(rot)), m) in valid_points else T_free_stream
            T4 = sp.Symbol(f'T{n}{int(m - np.sin(rot))}') if (n, int(m - np.sin(rot))) in valid_points else T_free_stream
            eq = T1 + T2 + T3 + T4 - 2*(3 + h*delta_x/k)*T + 2*(h*delta_x/k)*T_free_stream
        elif point_type == 'planar':
            T1 = 2 * (sp.Symbol(f'T{int(n - np.cos(rot))}{m}') if (int(n - np.cos(rot)), m) in valid_points else T_free_stream)
            T2 = 2 * (sp.Symbol(f'T{n}{int(m + np.sin(rot))}') if (n, int(m + np.sin(rot))) in valid_points else T_free_stream)
            T3 = 2 * (sp.Symbol(f'T{n}{int(m - np.sin(rot))}') if (n, int(m - np.sin(rot))) in valid_points else T_free_stream)
            eq = T1 + T2 + T3 - 2*(2 + h*delta_x/k)*T + 2*(h*delta_x/k)*T_free_stream
        elif point_type == 'exterior_corner':
            T1 = sp.Symbol(f'T{int(n - np.cos(rot))}{m}') if (int(n - np.cos(rot)), m) in valid_points else T_free_stream
            T2 = sp.Symbol(f'T{n}{int(m - np.sin(rot))}') if (n, int(m - np.sin(rot))) in valid_points else T_free_stream
            eq = T1 + T2 - 2*(2 + h*delta_x/k)*T + 2*(h*delta_x/k)*T_free_stream
        else:
            # fallback
            T_up    = sp.Symbol(f'T{n}{m+1}') if (n, m+1) in valid_points else T_free_stream
            T_down  = sp.Symbol(f'T{n}{m-1}') if (n, m-1) in valid_points else T_free_stream
            T_right = sp.Symbol(f'T{n+1}{m}') if (n+1, m) in valid_points else T_free_stream
            T_left  = sp.Symbol(f'T{n-1}{m}') if (n-1, m) in valid_points else T_free_stream
            eq = T_up + T_down + T_right + T_left - 4*T

        point.attributes['equation'] = eq
        point.attributes['label'] = T
        print(f"Point({n},{m}), type={point_type}, source={is_source}: sp.Eq({eq},0)")


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