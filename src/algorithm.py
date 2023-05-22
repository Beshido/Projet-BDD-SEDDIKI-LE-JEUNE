from contraintes import TGD, EGD

MAX_ITERATIONS = 100

def standard_chase(contraintes: list, tables: list) -> bool:
    iteration = 0
    found_new_solution = False
    while not found_new_solution or iteration < MAX_ITERATIONS:
        found_new_solution = True
        for contrainte in contraintes:
            for table in tables:
                if contrainte.is_satisfied_by(table) and not contrainte.is_head_satisfied_by(table) and not contrainte.is_applied_to(table):
                    if isinstance(contrainte, TGD):
                        contrainte.add_missing_tuples(table)
                    elif isinstance(contrainte, EGD):
                        contrainte.equalize(table)
                    else:
                        raise Exception("Unknown constraint type")
                    contrainte.apply_to(table)
                    found_new_solution = False
        iteration += 1
    
    return all(e.is_satisfied_by(table) for e in contraintes for table in tables)

def oblivious_chase(contraintes: list, tables: list) -> bool:
    iteration = 0
    while iteration < MAX_ITERATIONS:
        for contrainte in contraintes:
            for table in tables:
                if contrainte.is_satisfied_by(table) and not contrainte.is_head_satisfied_by(table) :
                    if isinstance(contrainte, TGD):
                        contrainte.add_missing_tuples(table)
                    elif isinstance(contrainte, EGD):
                        raise Exception("EGD pas compatible avec l'oblivious chase")
                    else:
                        raise Exception("Type de contrainte inconnu")
        iteration += 1
                   
    return all(e.is_satisfied_by(table) for e in contraintes for table in tables)