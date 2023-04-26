from constraints import *
from typing import List, Set, Tuple

def standard_chase(D, sigma):
    """
    Vérifie si la base de données D satisfait l'ensemble de contraintes sigma en utilisant l'algorithme Standard Chase.
    :param D: la base de données à vérifier
    :param sigma: l'ensemble de contraintes à vérifier
    :return: True si D satisfait sigma, False sinon
    """
    while True:
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
    return all(e.is_satisfied_by(D) for e in sigma)

class Database:
    def __init__(self, relations=None, constraints=None):
        self.relations = relations or {}
        self.constraints = constraints or []

    def is_conformant(self):
        """
        Vérifie si la base de données est conforme aux contraintes en utilisant l'algorithme Standard Chase.
        :return: True si la base de données est conforme, False sinon
        """
        return standard_chase(self.get_tuples(), self.constraints)
    
    def get_tuples(self):
        """
        Retourne l'ensemble de tous les tuples de toutes les relations de la base de données.
        :return: un ensemble de tuples
        """
        return set.union(*[self.relations[rel] for rel in self.relations])

    def print_database(self):
        for rel_name, rel in self.relations.items():
            print(rel)