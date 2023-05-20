from contraintes import *
from main import *

def oblivious_chase(contraintes : list, tables : list, arret=None) -> bool :
    iteration = 0
    while arret is None or iteration < arret :
        found_new_solution = False
        for contrainte in contraintes :
            for table in tables :
                if contrainte.is_satisfied_by(table) and not contrainte.is_head_satisfied_by(table) :
                    if isinstance(contrainte, TGD) :
                        contrainte.add_missing_tuples(table)
                    elif isinstance(contrainte, EGD) :
                        continue
                    else :
                        raise Exception("Type de contrainte inconnu")
                    found_new_solution = True
                    
    return all(e.is_satisfied_by(table) for e in contraintes for table in tables)