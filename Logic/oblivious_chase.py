from standard_chase import *

def oblivious_chase(D, sigma, max_iterations=None):
    """
    Vérifie si la base de données D satisfait l'ensemble de contraintes sigma en utilisant l'algorithme Oblivious Chase.
    L'algorithme effectue au maximum max_iterations tours de boucle (ou jusqu'à ce que la saturation soit atteinte).
    :param D: la base de données à vérifier
    :param sigma: l'ensemble de contraintes à vérifier
    :param max_iterations: le nombre maximum de tours de boucle à effectuer, à estimer en fonction du temps d'exécution avec un max_ierations faible
    :return: True si D satisfait sigma, False sinon
    """
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