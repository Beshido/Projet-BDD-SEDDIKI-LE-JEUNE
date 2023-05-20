from typing import List, Tuple

class Database:
    def __init__(self, relations=None, constraints=None):
        self.relations = relations or {}
        self.constraints = constraints or []

    def is_conformant(self):
        """
        Vérifie si la base de données est conforme aux contraintes en utilisant l'algorithme Standard Chase.
        :return: True si la base de données est conforme, False sinon
        """
        return standard_chase(self)
    
    def get_tuples(self):
        """
        Retourne l'ensemble de tous les tuples de toutes les relations de la base de données.
        :return: un ensemble de tuples
        """
        tuples = {}
        for _, rel in self.relations.items():
            tuples[rel.name] = rel.get_tuple()
        return tuples

    def print_database(self):
        for rel_name, rel in self.relations.items():
            print(rel)

class Attribute:
    def __init__(self, name: str, relation_name: str):
        self.name = name
        self.relation_name = relation_name

class Relation:
    def __init__(self, name: str, attr: tuple, keys: tuple, *content: tuple):
        self.name = name
        self.attr = attr
        self.keys = keys
        self.content = list(content)
    
    def get_tuple(self):
        d = []
        for tuple in self.content:
            current_element = {}
            for attr, value in zip(self.attr, tuple):
                current_element[attr] = value
            d.append(current_element)
        return d

    def content_as_dict(self):
        list = []
        for line in self.content:
            d = {}
            for key, attr, value in zip(self.keys, self.attr, line):
                d[attr] = value
            list.append(d)
        return list

    def tuple_to_dict(self, line: tuple):
        d = {}
        for _, attr, value in zip(self.keys, self.attr, line):
            d[attr] = value
        return d


    def contains(self, line: dict):
        for item in self.content:
            for index, keys in enumerate(self.keys):
                if keys:
                    attr_name = self.attr[index]
                    if item[index] != line[attr_name]:
                        continue
            return True
        return False

    def __str__(self):
        tuples_str = "\n".join(str(t) for t in self.content)
        return f"{self.name}:\n{tuples_str}"

class TGD:
    def __init__(self, database: Database, source: str, where: tuple, default: str):
        self.database = database
        self.source = source
        self.where = where
        self.default = default
        self.applied_to = set()

    def is_satisfied_by(self, line: dict):
        data = self.database.relations[self.source]
        if data.contains(line):
            return True
        return True

    def is_head_satisfied_by(self, line: dict):
        for location in self.where:
            data = self.database.relations[location]
            if data.contains(line):
                return True
        return False

    def mark_applied(self, tuple):
        self.applied_to.add(tuple)

    def is_applied_to(self, tuple):
        return tuple in self.applied_to

    def get_new_tuple(self, t: dict):
        new_t = {}
        for attr in self.database.relations[self.default].attr:
            new_t[attr] = t.get(attr, (None, False))
        return new_t

    def get_relation_name(self, attr: str) -> int:
        for i, attribute in enumerate(self.lhs):
            if attribute == attr:
                return i
        return -1

class EGD:
    def __init__(self, database: Database, source: str, lhs: List[Attribute], rhs: List[lambda _: bool], update: bool = False, expected_rhs: List[lambda _: _] = None):
        self.source = source
        self.lhs = lhs
        self.rhs = rhs
        self.update = update
        self.expected_rhs = expected_rhs
        self.applied_to = set()

    def is_satisfied_by(self, tuple):
        for attribute in self.lhs:
            if self.source not in tuple or attribute not in tuple[self.source]:
                return False
        return True
    
    def is_head_satisfied_by(self, tuple):
        for left_attribute, function in zip(self.lhs, self.rhs):
            if self.source not in tuple:
                return False
            if not self.update:
                if function(tuple[self.source]) == False:
                    return False
            else:
                if function(tuple[self.source] != tuple[self.source][left_attribute]):
                    return False
        return True
    
    def equalize(self, tuple):
        for attribute, function in zip(self.lhs, self.rhs):
            if not self.update:
                if function(tuple[self.source]) == False:
                    tuple[self.source][attribute] = None
            else:
                if function(tuple[self.source]) != tuple[self.source][attribute]:
                    tuple[self.source][attribute] = function(tuple[self.source])

    def mark_applied(self, tuple):
        self.applied_to.add(tuple)

    def is_applied_to(self, content: tuple):
        return content in self.applied_to

    def get_attribute_value(self, attr: Attribute, t: List[Tuple[str]]) -> str:
        for attribute in t:
            if attribute[0] == attr.name and attribute[1] == attr.relation_name:
                return attribute[2]
        return ""

def standard_chase(D: Database):
    """
    Vérifie si la base de données D satisfait l'ensemble de contraintes sigma en utilisant l'algorithme Standard Chase.
    :param D: la base de données à vérifier
    :param sigma: l'ensemble de contraintes à vérifier
    :return: True si D satisfait sigma, False sinon
    """
    while True:
        found_new_solution = False
        new_tuples = []  # Nouveaux tuples ajoutés à chaque itération
        for e in D.constraints:
            for T, T_DICT in zip(D.relations[e.source].content, D.relations[e.source].content_as_dict()):
                if e.is_satisfied_by(T_DICT) and not e.is_head_satisfied_by(T_DICT) and not e.is_applied_to(T):
                    if isinstance(e, TGD):
                        u = e.get_new_tuple(T_DICT)
                        if not D.relations[e.default].contains(u):  # Vérifier si le nouveau tuple est déjà présent dans D
                            new_tuples.append(u)  # Ajouter le nouveau tuple à la liste des nouveaux tuples
                            e.mark_applied(T)
                            found_new_solution = True
                    elif isinstance(e, EGD):
                        e.equalize(T_DICT)
                        e.mark_applied(T_DICT)
                        found_new_solution = True
        if not found_new_solution:
            break
        D.extend(new_tuples)  # Ajouter les nouveaux tuples à la base de données
    return all(
        e.is_satisfied_by(D.relations[e.source].tuple_to_dict(T)) 
        for e in D.constraints
        for T in D.relations[e.source].content)