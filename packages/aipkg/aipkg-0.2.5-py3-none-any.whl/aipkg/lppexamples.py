import scipy
# # Question 1

# - Machine X1 costs \$50/hour to run, 5 units of labour required per hour, produces 10 units of output per hour
# - Machine X2 costs \$80/hour to run, 2 units of labour required per hour, produces 12 units of output per hour
# - 20 units of labour available
# - 90 units of output required

# Minimize costs.

# Cost Function: 50x1 + 80x2
# Constraint 1: 5x1 + 2x2 <= 20
# Constraint 2: 10x1 + 12x2 >= 90   ==>   - 10x1 - 12x2 <= -90

result = scipy.optimize.linprog(
    [50, 80],                         # cost function
    A_ub = [[5,2], [-10,-12]],        # coefficients for inequalities
    b_ub = [20, -90])                 # constraints for inequalities

if result.success:
    print(f'X1: {round(result.x[0], 2)} hours')
    print(f'X2: {round(result.x[1], 2)} hours')
else:
    print('No Solution')

###################################################################################################

# # Question 2

# - Tables take 10 units of lumber, 5 hours of labour, make you a profit of \$180
# - Bookcases take 20 units of lumber, 4 hours of labour, make you a profit of \$200
# - 200 units of lumber available 
# - 80 hours of labour available

# Maximize the profits of the carpenter

# Optimization Function: 180x1 + 200x2
# Constraint 1: 10x1 + 20x2 <= 200
# Constraint 2: 5x1 + 4x2 <= 80

result = scipy.optimize.linprog(
    [-180,-200],
    A_ub = [[10,20], [5,4]],
    b_ub = [200,80])

if result.success:
    print(f'Tables: {round(result.x[0], 2)}')
    print(f'Tables: {round(result.x[1], 2)}')
else:
    print('No Solution')

###################################################################################################

# # Question 3

# A farmer has recently acquired a 110 hectares piece of land. He has decided to grow wheat and barley on that land. 
# Due to the quality of the sun and the region's excellent climate, the entire production of Wheat and Barley can be sold. 
# He wants to know how to plant each variety in the 110 hectares, given the costs, net profits and labor requirements according to the data shown below:

# |Variety|Cost (Price/Hec)|Net Profit (Price/Hec)|Man-days/Hec|
# | --- | --- | --- | --- |
# |Wheat|100|50|10|
# |Barley|200|120|30|

# The farmer has a budget of US$10,000 and availability of 1,200 man-days during the planning horizon. Find the optimal solution and the optimal value.

# Optimization Function: 50x1 + 120x2
# Constraint 1: 100x1 + 200x2 <= 10000
# Constraint 2: 10x1 + 30x2 <= 1200
# Constraint 3: x1 + x2 <= 110

result = scipy.optimize.linprog(
    [-50,-120],
    A_ub = [[100,200], [10,30], [1,1]],
    b_ub = [10000, 1200, 110])

if result.success:
    print(f'Wheat: {round(result.x[0], 2)} Hectares')
    print(f'Barley: {round(result.x[1], 2)} Hectares')
else:
    print('No Solution')

###################################################################################################

# # Question 4

# A toy manufacturing organization manufactures two types of toys A and B. Both the toys are sold at Rs.25 and Rs.20 respectively.
# There are 2000 resource units available every day from which the toy A requires 20 units while toy B requires 12 units. 
# Both of these toys require a production time of 5 minutes. Total working hours are 9 hours a day. 
# What should be the manufacturing quantity for each of the pipes to maximize the profits?

# Z = 25x1 + 20x2

# Objective: Max(Z)

# 20x1 + 12x2 <= 2000

# 5x1 + 5x2 <= 540
# Optimization Function: 25x1 + 20x2
# Constraint 1: 20x1 + 12x2 <= 2000
# Constraint 2: 5x1 + 5x2 <= 540

result = scipy.optimize.linprog(
    [-25,-20],
    A_ub = [[20,12], [5,5]],
    b_ub = [2000,540])

if result.success:
    print(f'Toy 1: {round(result.x[0], 2)} Units')
    print(f'Toy 2: {round(result.x[1], 2)} Units')
else:
    print('No Solution')

###################################################################################################

# # Question 5

# Say that a factory produces four different products, and that the daily produced amount of the first product is x₁, 
# the amount produced of the second product is x₂, and so on. The goal is to determine the profit-maximizing daily production amount for each product, 
# bearing in mind the following conditions:

# 1. The profit per unit of product is USD 20, USD 12, USD 40, and USD 25 for the first, second, third, and fourth product, respectively.

# 2. Due to manpower constraints, the total number of units produced per day can’t exceed fifty.

# 3. For each unit of the first product, three units of the raw material A are consumed. 
# Each unit of the second product requires two units of the raw material A and one unit of the raw material B. 
# Each unit of the third product needs one unit of A and two units of B. Finally, each unit of the fourth product requires three units of B.

# 4. Due to the transportation and storage constraints, the factory can consume up to one hundred units of the raw material A and ninety units of B per day.

# Optimization Function: 20x1 + 12x2 + 40x3 + 25x4
# Constraint 1: x1 + x2 + x3 + x4 <= 50
# Constraint 2: 3x1 + 2x2 + x3 <= 100
# Constraint 3: x2 + 2x3 + 3x4 <= 90

result = scipy.optimize.linprog(
    [-20,-12,-40,-25],
    A_ub = [[1,1,1,1], [3,2,1,0], [0,1,2,3]],
    b_ub = [50, 100, 90])

if result.success:
    print(f'X1: {round(result.x[0], 2)} Units')
    print(f'X2: {round(result.x[1], 2)} Units')
    print(f'X3: {round(result.x[2], 2)} Units')
    print(f'X4: {round(result.x[3], 2)} Units')

###############################################################################

# Q. A toy manufacturing organization manufactures two types of toys A and B. Both the toys are sold at Rs.25 and Rs.20 respectively. 
# There are 2000 resource units available every day from which the toy A requires 20 units while toy B requires 12 units. 
# Both of these toys require a production time of 5 minutes. Total working hours are 9 hours a day. 
# What should be the manufacturing quantity for each of the pipes to maximize the profits?

# Z = 25x1 + 20x2

# Objective: Max(Z)

# 20x1 + 12x2 <= 2000

# 5x1 + 5x2 <= 540

# ANSWER] 

x1_bounds = (0,None)
x2_bounds = (0,None)

result = scipy.optimize.linprog(
    [-25, -20],  # Cost function: 50x_1 + 80x_2
    A_ub=[[20, 12], [5, 5]],  # Coefficients for inequalities
    b_ub=[2000, 540],  # Constraints for inequalities: 20 and -90
    bounds=[x1_bounds,x2_bounds]
)

if result.success:
    print(f"X1: {round(result.x[0], 2)} units")
    print(f"X2: {round(result.x[1], 2)} units")
else:
    print("No solution")


############

# Q. A farmer has recently acquired a 110 hectares piece of land. He has decided to grow Wheat and barley on that land. 
# Due to the quality of the sun and the regions excellent climate, the entire production of Wheat and Barley can be sold. 
# He wants to know how to plant each variety in the 110 hectares, given the costs, net profits and labor requirements according to the data shown below:

# |Variety|Cost (Price/Hec)|Net Profit (Price/Hec)|Man-days/Hec|
# | --- | --- | --- | --- |
# |Wheat|100|50|10|
# |Barley|200|120|30|

# The farmer has a budget of US$10,000 and availability of 1,200 man-days during the planning horizon. Find the optimal solution and the optimal value.


# ANSWER ] 


x1_bounds = (0,None)
x2_bounds = (0,None)

result = scipy.optimize.linprog(
    [-50, -120],  # Cost function: 50x_1 + 80x_2
    A_ub=[[100, 200], [10, 30], [1,1]],  # Coefficients for inequalities
    b_ub=[10000, 1200, 110],  # Constraints for inequalities: 20 and -90
    bounds=[x1_bounds,x2_bounds]
)

if result.success:
    print(f"X1: {round(result.x[0], 2)} Hectares of Wheat")
    print(f"X2: {round(result.x[1], 2)} Hectares of Barley")
else:
    print("No solution")


