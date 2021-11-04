"""
Implementation of the gaussian elimination by l-u-decomposition. The implementation is straight forward, hence, no
commentaries.
"""


def gaussian_elimination(matrix, b):
    l_u = l_u_decomposition(matrix)
    u_matrix = l_u[0]
    l_matrix = l_u[1]
    c_vector = calc_c_vector(l_matrix, b)
    return calc_solution_vector(u_matrix, c_vector)


def calc_solution_vector(u_matrix, c_vector):
    solution_vector = [c_vector[-1] / u_matrix[-1][-1]]
    number_of_columns = 0
    for i in range(2, len(u_matrix)+1):
        intermediate = c_vector[-i]
        number_of_columns += 1
        for j in range(0, number_of_columns):
            intermediate = intermediate - solution_vector[-(j+1)] * u_matrix[-i][-(j+1)]
        solution_vector.append(intermediate / u_matrix[-i][-(number_of_columns+1)])
        solution_vector.reverse()
    return solution_vector


def calc_c_vector(l_matrix, b):
    c_vector = [b[0] / l_matrix[0][0]]
    number_of_columns = 0
    for i in range(1, len(l_matrix)):
        intermediate = b[i]
        number_of_columns += 1
        for j in range(0, number_of_columns):
            intermediate = intermediate - c_vector[j] * l_matrix[i][j]
        c_vector.append(intermediate / l_matrix[i][number_of_columns])
    return c_vector


def l_u_decomposition(matrix):
    u_matrix = partial_pivot(matrix)
    l_matrix = []
    # fill diagonal of u with 1's
    for i in range(0, len(u_matrix)):
        row = []
        for j in range(0, len(u_matrix[0])):
            if j == i:
                row.append(1)
            else:
                row.append(0)
        l_matrix.append(row)

    for n in range(0, len(u_matrix) - 1):
        pivot_element = u_matrix[n][n]
        for k in range(n+1, len(u_matrix)):
            multiplicand = u_matrix[k][n] / pivot_element
            l_matrix[k][n] = multiplicand
            for j in range(0, len(l_matrix[k])):
                if j <= n:
                    u_matrix[k][j] = 0
                else:
                    u_matrix[k][j] = u_matrix[k][j] - u_matrix[k - 1][j] * multiplicand

    return u_matrix, l_matrix


def partial_pivot(matrix):
    sorted_matrix = []
    for i in range(0, len(matrix[0])):
        max = matrix[0][i]
        max_index = 0
        for j in range(len(matrix)):
            if matrix[j][i] > max:
                max_index = j
        sorted_matrix.append(matrix.pop(max_index))
    return sorted_matrix


if __name__ == '__main__':
    print(gaussian_elimination([[1, 1, 2],
                          [-1, 2, 1],
                          [0, -1, 1]], [1, 2, 3]))
