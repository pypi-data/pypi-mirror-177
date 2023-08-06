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
    if len(assignment) == len(VARIABLES):
        return assignment

    # Try a new variable
    var = select_unassigned_variable(assignment)
    for value in domain:
        new_assignment = assignment.copy()
        new_assignment[var] = value
        print("Assigning ", var, "= ", value) # Only for explaination
        if consistent(new_assignment):
            print(var, " :Yes Consistent")
            result = backtrack(new_assignment)
            if result is not None:
                return result
        print(var, " :No not consistent")  # Only for explaination
    return None


def select_unassigned_variable(assignment):
    """Chooses a variable not yet assigned, in order."""
    for variable in VARIABLES:
        if variable not in assignment:
            return variable
    return None


def consistent(assignment):
    """Checks to see if an assignment is consistent."""
    for (x, y) in CONSTRAINTS:

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






