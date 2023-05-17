from typing import Dict, List, Tuple
from standard_chase import Database

class Attribute:
    def __init__(self, name: str, relation_name: str):
        self.name = name
        self.relation_name = relation_name

class Relation:
    def __init__(self, name, *tuples):
        self.name = name
        self.attr = tuples[0]
        self.tuples = tuples[1:]
    
    def get_tuple(self):
        d = []
        for tuple in self.tuples:
            current_element = {}
            for attr, value in zip(self.attr, tuple):
                current_element[attr] = value
            d.append(current_element)
        return d

    def __str__(self):
        tuples_str = "\n".join(str(t) for t in self.tuples)
        return f"{self.name}:\n{tuples_str}"


class TGD:
    def __init__(self, lhs: List[Attribute], rhs: List[Attribute]):
        self.lhs = lhs
        self.rhs = rhs
        self.applied_to = set()

    def is_satisfied_by(self, tuple):
        relation_name = self.lhs[0].relation_name
        if relation_name not in tuple:
            return False
        for attribute in self.lhs:
            if attribute.name not in tuple[relation_name]:
                return False
        return True

    def is_head_satisfied_by(self, tuple):
        relation_name = self.rhs[0].relation_name
        if relation_name not in tuple:
            return False
        for attribute in self.rhs:
            if attribute.name not in tuple[relation_name]:
                return False
        return True

    def mark_applied(self, tuple):
        self.applied_to.add(tuple)

    def is_applied_to(self, tuple):
        return tuple in self.applied_to

    def get_new_tuple(self, t: List[Tuple[str]], d: List[List[Tuple[str]]]) -> List[Tuple[str]]:
        new_t = t.copy()
        for a in self.rhs:
            if a not in new_t:
                rel_name = self.get_relation_name(a)
                rel = d[rel_name]
                new_t += rel[0]
        return new_t

    def get_relation_name(self, attr: Attribute) -> int:
        for i, attribute in enumerate(self.lhs):
            if attribute.name == attr.name and attribute.relation_name == attr.relation_name:
                return i
        return -1

class EGD:
    def __init__(self, lhs: List[Attribute], rhs: List[Attribute]):
        self.lhs = lhs
        self.rhs = rhs
        self.applied_to = set()

    def is_satisfied_by(self, tuple):
        for attribute in self.lhs:
            relation_name = attribute.relation_name
            if relation_name not in tuple or attribute.name not in tuple[relation_name]:
                return False
        for attribute in self.rhs:
            relation_name = attribute.relation_name
            if relation_name not in tuple or attribute.name not in tuple[relation_name]:
                return False
        return True

    def mark_applied(self, tuple):
        self.applied_to.add(tuple)

    def is_applied_to(self, tuple):
        return tuple in self.applied_to

    def get_attribute_value(self, attr: Attribute, t: List[Tuple[str]]) -> str:
        for attribute in t:
            if attribute[0] == attr.name and attribute[1] == attr.relation_name:
                return attribute[2]
        return ""