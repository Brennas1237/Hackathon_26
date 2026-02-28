import sympy as sp
import numpy as np
import Point



def make_equation_list(point_list):
    equation_list = []
    for point in point_list:
        equation = point.equation
        equation_list.append(equation)
    return equation_list

def make_variable_list(point_list):
    variable_list = []
    for point in point_list:
        variable = point.variable
        variable_list.append(variable)

def solve_system(equation_list, variable_list):
    coefficient_matrix, solution_vector = sp.linear_eq_to_matrix(equation_list, variable_list)
    coefficient_matrix = sp.matrix2numpy(coefficient_matrix, dtype=float)
    solution_vector = sp.matrix2numpy(solution_vector, dtype=float)
    temperature_list = np.linalg.solve(coefficient_matrix, solution_vector)
    return temperature_list

