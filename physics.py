import sympy as sp
import numpy as np
# import T_free_stream, h, delta_x, k



def set_equaiton(point):
    n = point.x
    m = point.y
    rot = point.rotation
    eq = 0

    T, T1, T2, T3, T4 = sp.symbols('T, T1, T2, T3, T4')
    # T = T(n,m)
    # T1 = T(n + cos(rot), m)
    # T2 = T(n, m + sin(rot))
    # T3 = T(n - cos(rot), m)
    # T4 = T(n, m - sin(rot))

    if point.missing_count == 0 and n == 0:
        eq = T - T_base
    elif point.missing_count == 0 and n != 0:
        eq = T1 + T2 + T3 + T4 - 4 * T
    elif point.missing_count == 1:
        eq = 2 * (T3 + T4) + T1 + T2 - 2 * (3 + h * delta_x / k) * T + 2 * (h * delta_x / k) * T_free_stream
    elif point.missing_count == 2:
        eq = 2 * T3 + T2 + T4 - 2 * (2 + h * delta_x / k) * T + 2 * (h * delta_x / k) * T_free_stream
    elif point.missing_count == 3:
        eq = T4 + T3 - 2 * (2 + h * delta_x / k) * T + 2 * (h * delta_x / k) * T


