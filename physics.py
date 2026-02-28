import sympy as sp
import numpy as np


def set_equaiton(point):
    n = point.x
    m = point.y
    rotation = point.rotation

    if point.type == "root":
        eq = sp
