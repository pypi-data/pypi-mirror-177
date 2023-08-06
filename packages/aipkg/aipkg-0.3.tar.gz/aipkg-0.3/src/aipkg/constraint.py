"""
Naive backtracking search without any heuristics or inference.
"""

VARIABLES = ["A", "B", "D", "E", "C", "F", "G"]
domain = ["Monday", "Tuesday", "Wednesday"]

CONSTRAINTS = [
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("B", "D"),
    ("B", "E"),
    ("D", "E"),
    ("C", "E"),
    ("C", "F"),
    ("E", "F"),
    ("E", "G"),
    ("F", "G")
]

def backtrack(assignment):
    """Runs backtracking search to find an assignment."""

    # Check if assignment is complete
    if len(assignment) == len(VARIABLES): # If every variable is assigned to a value
        return assignment # Return the assignment

    # Try a new variable
    var = select_unassigned_variable(assignment) # Select an unassigned variable from the assignment
    for value in domain: # For each possible value in the domain
        
        # Create a new assignement that assigns variable to the value
        new_assignment = assignment.copy() # New assignement creation
        new_assignment[var] = value # assigning variable to the value

        print("Assigning ", var, "= ", value) # Check if assignment is complete (line 35)
        if consistent(new_assignment): # Checking if the new assignment is consistent
            print(var, " :Yes Consistent") #Verifying consistency via a print statement
            result = backtrack(new_assignment) # If consistent, call backtrack to continue backtrack search
            if result is not None: # As long as result is not a failure (None)
                return result # Return the result
        print(var, " :No not consistent")  # Only for explaination
    return None # In case of no solution, declare it a failure by returning None


def select_unassigned_variable(assignment):
    """Chooses a variable not yet assigned, in order."""
    for variable in VARIABLES: # Looping over all variables
        if variable not in assignment: # If the varialbe is not assigned already, then return the variable
            return variable 
    return None


def consistent(assignment):
    """Checks to see if an assignment is consistent."""
    for (x, y) in CONSTRAINTS: # Check constraints

        # Only consider arcs where both are assigned
        if x not in assignment or y not in assignment:
            continue

        # If both have same value, then not consistent
        if assignment[x] == assignment[y]:
            return False 

    # If nothing inconsistent, then assignment is consistent
    return True

assignment = dict()
solution = backtrack(assignment)
print(solution)






