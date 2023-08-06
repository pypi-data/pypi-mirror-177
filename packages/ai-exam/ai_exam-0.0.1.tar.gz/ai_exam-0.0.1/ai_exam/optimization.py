def optimization():
    print('''
    variables=["A","B","D","E","C","F","G"]
domains=["Monday","Tuesday","Wednesday"]
constraints=[("A","B"),
            ("A","C"),
            ("B", "C"),
            ("B", "D"),
            ("B", "E"),
            ("D", "E"),
            ("C", "E"),
            ("C", "F"),
            ("E", "F"),
            ("E", "G"),
            ("F", "G")]
def backtrack(assignment):
    if len(assignment)==len(variables):
        return assignment
    var=select_unassigned_variable(assignment)
    for value in domains:
        new_assignment=assignment.copy()
        new_assignment[var]=value
        if consistent(assignment):
            print(var, ': Yes consistent')
            result=backtrack(new_assignment)
            if result is not None:
                return result
            
        print(var,': Not consistent')
    return None

def select_unassigned_variable(assignment):
    for variable in variables:
        if variable not in assignment:
            return variable
    return None

def consistent(assignment):
    for x,y in constraints:
        if x not in assignment or y not in assignment:
            continue
        if assignment[x]==assignment[y]:
            return False
    return True
    
assignment=dict()
solution=backtrack(assignment)
print(solution)''')

optimization()