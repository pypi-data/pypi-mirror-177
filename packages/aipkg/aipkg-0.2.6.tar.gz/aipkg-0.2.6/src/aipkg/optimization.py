from scipy.optimize import linprog

# Objective Function: 50x_1 + 80x_2
# Constraint 1: 5x_1 + 2x_2 <= 20
# Constraint 2: -10x_1 + -12x_2 <= -90

result = linprog(
    [50, 80],  # Cost function: 50x_1 + 80x_2
    A_ub = [[5, 2], [-10, -12]],  # Coefficients of the inequalites
    b_ub = [20, -90],  # Coefficients of the inequalities: 20 and -90
)

if result.success:
    print(f"X1: {round(result.x[0], 2)} hours")
    print(f"X2: {round(result.x[1], 2)} hours")
else:
    print("No solution")

# n_t = number of tables
# n_b = number of bookcases

# Function to maximise: 180n_t + 200n_b
# Function to minimize: -180n_t - 200n_b
# 10n_t + 20n_b <= 200
# 5n_t + 4n_b = 80

result = linprog(
    [-180, -200],
    A_ub = [[10, 20], [5, 4]],
    b_ub=[200, 80]
)

if result.success:
    print(f"X1: {round(result.x[0], 2)} units of lumber")
    print(f"X2: {round(result.x[1], 2)} hours of labour")
else:
    print("No result found")

