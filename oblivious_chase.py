from standard_chase import standard_chase

def oblivious_chase(D, sigma, max_iterations=None):
    i = 0
    while max_iterations is None or i < max_iterations:
        found_new_solution = False
        for e in sigma:
            for T in D:
                if e.is_satisfied_by(T) and not e.is_head_satisfied_by(T) and not e.is_applied_to(T):
                    if isinstance(e, TGD):
                        u = e.get_new_tuple(T)
                        D.append(u)
                        e.mark_applied(T)
                        found_new_solution = True
                    elif isinstance(e, EGD):
                        e.equalize(T)
                        e.mark_applied(T)
                        found_new_solution = True
        if not found_new_solution:
            break
        i += 1
    return all(e.is_satisfied_by(D) for e in sigma)