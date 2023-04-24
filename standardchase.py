class Variable:
    """
    Classe pour représenter une variable dans une contrainte.
    """

    def __init__(self, name: str, index: int):
        """
        Initialise une variable avec son nom et son indice.

        :param name: Le nom de la variable.
        :param index: L'indice de la variable.
        """
        self.name = name
        self.index = index

    def __eq__(self, other):
        """
        Vérifie si deux variables sont égales.

        :param other: L'autre variable à comparer.
        :return: True si les deux variables sont égales, False sinon.
        """
        return isinstance(other, Variable) and self.name == other.name and self.index == other.index

    def __hash__(self):
        """
        Calcule le hash de la variable.

        :return: Le hash de la variable.
        """
        return hash((self.name, self.index))

    def __str__(self):
        """
        Convertit la variable en chaîne de caractères.

        :return: La chaîne de caractères représentant la variable.
        """
        return f"{self.name}{self.index}"


class Constant:
    """
    Classe pour représenter une constante dans une contrainte.
    """

    def __init__(self, value):
        """
        Initialise une constante avec sa valeur.

        :param value: La valeur de la constante.
        """
        self.value = value

    def __eq__(self, other):
        """
        Vérifie si deux constantes sont égales.

        :param other: L'autre constante à comparer.
        :return: True si les deux constantes sont égales, False sinon.
        """
        return isinstance(other, Constant) and self.value == other.value

    def __hash__(self):
        """
        Calcule le hash de la constante.

        :return: Le hash de la constante.
        """
        return hash(self.value)

    def __str__(self):
        """
        Convertit la constante en chaîne de caractères.

        :return: La chaîne de caractères représentant la constante.
        """
        return f"{self.value}"

class TGD:
    def __init__(self, body, head):
        self.body = body
        self.head = head
        self.applied_to = set()

    def is_satisfied_by(self, tuple):
        return all(tuple[v.index] == c.value if isinstance(c, Constant) else True for v, c in zip(self.body, self.head))

    def is_head_satisfied_by(self, tuple):
        return all(tuple[v.index] == c.value if isinstance(c, Constant) else False for v, c in zip(self.body, self.head))

    def is_applied_to(self, tuple):
        return tuple in self.applied_to

    def mark_applied(self, tuple):
        self.applied_to.add(tuple)

    def get_new_tuple(self, tuple):
        return tuple + tuple[len(self.body):]

    def __str__(self):
        return f"{','.join(str(v) for v in self.body)} -> {','.join(str(c) for c in self.head)}"


class EGD:
    def __init__(self, variables):
        self.variables = variables
        self.applied_to = set()

    def is_satisfied_by(self, tuple):
        values = [tuple[v.index] if isinstance(v, Variable) else v.value for v in self.variables]
        return len(set(values)) == 1

    def is_applied_to(self, tuple):
        return tuple in self.applied_to

    def mark_applied(self, tuple):
        self.applied_to.add(tuple)

    def equalize(self, tuple):
        values = [tuple[v.index] for v in self.variables]
        for v in self.variables:
            tuple[v.index] = values[0]

    def __str__(self):
        return f"{','.join(str(v) for v in self.variables)}"
    
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
    def __init__(self, relations, constraints):
        """
        Initialise une base de données avec un ensemble de relations et de contraintes.
        :param relations: un dictionnaire où chaque clé est le nom d'une relation et chaque valeur est un ensemble de tuples
        :param constraints: une liste d'objets TGD et EGD représentant les contraintes de la base de données
        """
        self.relations = relations
        self.constraints = constraints
    
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

