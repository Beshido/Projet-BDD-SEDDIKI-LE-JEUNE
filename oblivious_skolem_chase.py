from standard_chase import *

def oblivious_skolem_chase(D, sigma):
    while True:
        found_new_solution = False
        for e in sigma:
            if isinstance(e, EGD):
                continue
            for T in D:
                if e.is_satisfied_by(T) and not e.is_head_satisfied_by(T) and not e.is_applied_to(T):
                    x = e.get_variables(T)
                    same_x_tuples = [t for t in D if e.is_satisfied_by(t) and e.get_variables(t) == x]
                    if len(same_x_tuples) == 1 or any(e.is_applied_to(t) for t in same_x_tuples):
                        continue
                    u = e.get_new_tuple(T, D)
                    D.append(u)
                    e.mark_applied(T)
                    found_new_solution = True
        if not found_new_solution:
            break
    return all(e.is_satisfied_by(D) for e in sigma)
