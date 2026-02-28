import sympy as sp
import numpy as np
import Point
# import T_free_stream, h, delta_x, k



def set_equaiton(point):
    n = point.x
    m = point.y
    rot = point.rotation
    eq = 0
    T = sp.Symbol('T' + str(n) + str(m))  # 00
    T1 = sp.Symbol('T' + str(n + int(np.cos(rot))) + str(m + int(np.sin(rot))))  # 10
    T2 = sp.Symbol('T' + str(n - int(np.sin(rot))) + str(m + int(np.cos(rot))))  # 01
    T3 = sp.Symbol('T' + str(n - int(np.cos(rot))) + str(m - int(np.sin(rot))))  # -10
    T4 = sp.Symbol('T' + str(n - int(np.sin(rot))) + str(m + int(np.cos(rot))))  # 0-1

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
    point.equation = eq
    point.lable = T
