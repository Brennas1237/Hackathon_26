import numpy as np
def solve_fin(L,w, dx, k=10, h=600, T_base=45, T_inf=25):
    length = L/1000
    width = w/1000

    delta_x = dx/1000

    x_domain = int(length // delta_x)
    y_domain = int(width // delta_x + 1)

    total_points = int(x_domain * y_domain)



    position_matrix = np.arange(0, total_points).reshape(y_domain, x_domain)
    matrix = np.zeros((total_points, total_points))
    sol_vect = np.zeros(total_points)

    row = 0
    for y in range(y_domain):
        for x in range(x_domain):
            if y == 0 and x == 0:
                matrix[row, int(position_matrix[y,x])] = -2 * (h * delta_x / k + 2)
                matrix[row, int(position_matrix[y,x + 1])] = 1
                matrix[row, int(position_matrix[y + 1 , x])] = 2
                sol_vect[row] = -T_base - (2*h*delta_x / k) * T_inf
            elif y == 0 and x != x_domain-1:
                matrix[row, int(position_matrix[y, x])] = -2 * (h * delta_x / k + 2)
                matrix[row, int(position_matrix[y, x + 1])] = 1
                matrix[row, int(position_matrix[y, x - 1])] = 1
                matrix[row, int(position_matrix[y + 1, x])] = 2
                sol_vect[row] = - (2 * h * delta_x / k) * T_inf
            elif y == 0 and x == x_domain-1:
                matrix[row, int(position_matrix[y, x])] = -2 * (h * delta_x / k + 1)
                matrix[row, int(position_matrix[y, x - 1])] = 1
                matrix[row, int(position_matrix[y + 1, x])] = 1
                sol_vect[row] =  - (2 * h * delta_x / k) * T_inf
            elif y != 0 and y != y_domain-1 and x == 0:
                matrix[row, int(position_matrix[y, x])] = -4
                matrix[row, int(position_matrix[y, x + 1])] = 1
                matrix[row, int(position_matrix[y + 1, x])] = 1
                matrix[row, int(position_matrix[y - 1, x])] = 1
                sol_vect[row] = -T_base
            elif y != 0 and y != y_domain-1 and x != x_domain-1:
                matrix[row, int(position_matrix[y, x])] = -4
                matrix[row, int(position_matrix[y, x + 1])] = 1
                matrix[row, int(position_matrix[y, x - 1])] = 1
                matrix[row, int(position_matrix[y + 1, x])] = 1
                matrix[row, int(position_matrix[y - 1, x])] = 1
                sol_vect[row] = 0
            elif y != 0 and y != y_domain-1 and x == x_domain-1:
                matrix[row, int(position_matrix[y, x])] = -2 * (h * delta_x / k + 2)
                matrix[row, int(position_matrix[y + 1, x])] = 1
                matrix[row, int(position_matrix[y - 1, x])] = 1
                matrix[row, int(position_matrix[y, x - 1])] = 2
                sol_vect[row] = - (2 * h * delta_x / k) * T_inf
            elif y == y_domain-1 and x == 0:
                matrix[row, int(position_matrix[y,x])] = -2 * (h * delta_x / k + 2)
                matrix[row, int(position_matrix[y,x + 1])] = 1
                matrix[row, int(position_matrix[y - 1 , x])] = 2
                sol_vect[row] = -T_base - (2*h*delta_x / k) * T_inf
            elif y == y_domain-1 and x != x_domain-1:
                matrix[row, int(position_matrix[y, x])] = -2 * (h * delta_x / k + 2)
                matrix[row, int(position_matrix[y, x + 1])] = 1
                matrix[row, int(position_matrix[y, x - 1])] = 1
                matrix[row, int(position_matrix[y - 1, x])] = 2
                sol_vect[row] = - (2 * h * delta_x / k) * T_inf
            elif y == y_domain-1 and x == x_domain-1:
                matrix[row, int(position_matrix[y, x])] = -2 * (h * delta_x / k + 1)
                matrix[row, int(position_matrix[y, x - 1])] = 1
                matrix[row, int(position_matrix[y - 1, x])] = 1
                sol_vect[row] =  - (2 * h * delta_x / k) * T_inf
            row += 1

    temp_distribution = (np.linalg.solve(matrix, sol_vect)).reshape(y_domain, x_domain)

    return temp_distribution
def fin_heat_convective(temp_distribution, dx, h=600, T_inf=25, thickness=1):
    delta_x = dx / 1000
    thickness = thickness

    Q = 0

    # Top surface
    Q += np.sum(h * (temp_distribution[0, :] - T_inf) * thickness * delta_x)

    # Bottom surface
    Q += np.sum(h * (temp_distribution[-1, :] - T_inf) * thickness * delta_x)

    # Tip (right side)
    Q += np.sum(h * (temp_distribution[:, -1] - T_inf) * thickness * delta_x)

    return Q
def convective_tip(L, w, k=10, h=600, T_base=45, T_inf=25, thickness=1):
    length = L/1000
    width = w/1000
    thickness = thickness
    perimeter = 2 * (width + thickness)
    area = width * thickness
    M = (T_base - T_inf) * np.sqrt(h * perimeter * k * area)
    m = np.sqrt((h * perimeter) / (k * area))
    q = M * (np.sinh(m*length) + (h / (m*k)) * np.cosh(m*length)) / (np.cosh(m*length) + (h / (m*k)) * np.sinh(m*length))
    return q
def insulated_tip(L, w, k=10, h=600, T_base=45, T_inf=25, thickness=1):
    length = L/1000
    width = w/1000
    thickness = thickness
    perimeter = 2 * (width + thickness)
    area = width * thickness
    M = (T_base - T_inf) * np.sqrt(h * perimeter * k * area)
    m = np.sqrt((h * perimeter) / (k * area))
    q = M * np.tanh(m*length)
    return q
length = 8
width = 1
dx = 1
print("For length =", length, "mm, width =", width, "mm, and Δx = Δy =", dx, "mm")
temperature_distributin = np.round(solve_fin(length,width,dx), decimals=1)
print("Matrix of temperature distribution (C)\n",temperature_distributin)
print("q per unit thickness:")
print("\tfrom FDM =", round(fin_heat_convective(temperature_distributin, dx), 3), "W/m")
print("\tconvective tip =", round(convective_tip(length, width), 3), "W/m")
print("\tinsulated tip =", round(insulated_tip(length, width), 3), "W/m")

