from standard_chase import *

def core_chase(D, sigma):
    """
    Calcule le noyau (core) de la base de données D pour l'ensemble de contraintes sigma en utilisant l'algorithme Core Chase.
    :param D: la base de données pour laquelle calculer le noyau
    :param sigma: l'ensemble de contraintes à vérifier
    :return: le noyau de D
    """
    while True:
        found_new_solution = False
        for T in D:
            D.remove(T)
            if is_satisfied(D, sigma):
                found_new_solution = True
            else:
                D.append(T)
        if not found_new_solution:
            break
    return D

def is_satisfied(D, sigma):
    """
    Vérifie si la base de données D satisfait l'ensemble de contraintes sigma.
    :param D: la base de données à vérifier
    :param sigma: l'ensemble de contraintes à vérifier
    :return: True si D satisfait sigma, False sinon
    """
    for e in sigma:
        if not e.is_satisfied_by(D):
            return False
    return True
