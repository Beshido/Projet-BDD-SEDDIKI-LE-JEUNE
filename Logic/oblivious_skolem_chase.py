from standard_chase import *

def oblivious_skolem_chase(database, sigma):
    """
    Modifie la base de données D afin qu'elle satisfasse l'ensemble de contraintes sigma en utilisant l'algorithme Skolem oblivious chase.
    :param database: la base de données à modifier
    :param sigma: l'ensemble de contraintes à satisfaire
    """
    while True:
        found_new_solution = False
        for e in sigma:
            for rel in database.relations.values():
                for t in rel.tuples:
                    if e.is_satisfied_by(t) and not e.is_head_satisfied_by(t) and not e.is_applied_to(t):
                        if isinstance(e, TGD):
                            u = e.get_new_tuple(t)
                            rel.add(u)
                            e.mark_applied(t)
                            found_new_solution = True
                        elif isinstance(e, EGD):
                            e.equalize(t)
                            e.mark_applied(t)
                            found_new_solution = True
        if not found_new_solution:
            break



