# physics.py
from math_module import set_equations, make_equation_list, make_variable_list, solve_system, assign_temp_to_point

def update_temperatures(point_list, T_base, T_free_stream, h, delta_x, k):
    # 1. Set symbolic equations for each point
    set_equations(point_list, T_base, T_free_stream, h, delta_x, k)

    # 2. Build lists
    eqs = make_equation_list(point_list)
    vars_ = make_variable_list(point_list)

    # 3. Solve
    temps = solve_system(eqs, vars_)

    # 4. Assign back to points
    assign_temp_to_point(point_list, temps)


