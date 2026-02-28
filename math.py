import sympy as sp
import numpy as np
import Point
from physics import set_equaiton
# import T_free_stream, h, delta_x, k


def make_equation_list(point_list):
    equation_list = []
    for point in point_list:
        equation = point.equation
        equation_list.append(equation)
    return equation_list

# def name_variables(surface max y, surface max x):
#     variable_list = []
#         for m in int(surface max y/delta_x)
#           for n in int(surface max x / delta_x):
#               variable = sp.Symbol("T" + str(n) + str(m))
#               variable_list.append(variable)
#   return

def solve(equation_list):
