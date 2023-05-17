from typing import Dict, List, Tuple
from standard_chase import Database

class Attribute:
    def __init__(self, name: str, relation_name: str):
        self.name = name
        self.relation_name = relation_name

class Relation:
    def __init__(self, name, *tuples):
        self.name = name
        self.tuples = list(tuples)

    def __str__(self):
        tuples_str = "\n".join(str(t) for t in self.tuples)
        return f"{self.name}:\n{tuples_str}"


class TGD:
    def __init__(self, lhs: List[Attribute], rhs: List[Attribute]):
        self.lhs = lhs
        self.rhs = rhs
        self.applied_to = set()

    def is_satisfied_by(self, database: Database) -> bool:
        relation_name = self.lhs[0].relation_name
        relation = database.relations.get(relation_name)
        if relation is None:
                return False
        for tuple in relation.tuples:
            if all(attr.name in tuple for attr in self.lhs):
                return True
        return False


    def is_head_satisfied_by(self, t: List[Tuple[str]]) -> bool:
        for a in self.rhs:
            if a not in t:
                return False
        return True

    def mark_applied(self, t: List[Tuple[str]]) -> None:
        self.applied_to.add(tuple(t))

    def is_applied_to(self, t: List[Tuple[str]]) -> bool:
        return tuple(t) in self.applied_to

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

    def is_satisfied_by(self, database: Database) -> bool:
        for relation in database.relations.values():
            for tuple in relation.tuples:
                lhs_values = [self.get_attribute_value(attr, tuple) for attr in self.lhs]
                rhs_values = [self.get_attribute_value(attr, tuple) for attr in self.rhs]
            if lhs_values != rhs_values:
                return False
        return True


    def get_attribute_value(self, attr: Attribute, t: List[Tuple[str]]) -> str:
        for attribute in t:
            if attribute[0] == attr.name and attribute[1] == attr.relation_name:
                return attribute[2]
        return ""

    def mark_applied(self, t: List[Tuple[str]]) -> None:
        self.applied_to.add(tuple(t))

    def is_applied_to(self, t: List[Tuple[str]]) -> bool:
        return tuple(t) in self.applied_to