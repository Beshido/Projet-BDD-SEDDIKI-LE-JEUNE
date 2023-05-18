from typing import List, Tuple

class Attribute:
    def __init__(self, name: str, relation_name: str):
        self.name = name
        self.relation_name = relation_name

class Relation:
    def __init__(self, name: str, attr: tuple, *content: tuple):
        self.name = name
        self.attr = attr
        self.content = list(content)
    
    def get_tuple(self):
        d = []
        for tuple in self.content:
            current_element = {}
            for attr, value in zip(self.attr, tuple):
                current_element[attr] = value
            d.append(current_element)
        return d

    def tuple_to_dict(self, line: tuple):
        d = {}
        for attr, value in zip(self.attr, line):
            d[attr] = value
        return {self.name: d}

    def __str__(self):
        tuples_str = "\n".join(str(t) for t in self.content)
        return f"{self.name}:\n{tuples_str}"


class TGD:
    def __init__(self, relation_name: str, lhs: List[Attribute], rhs: List[Attribute]):
        self.relation_name = relation_name
        self.lhs = lhs
        self.rhs = rhs
        self.applied_to = []

    def is_satisfied_by(self, tuple):
        if self.relation_name not in tuple:
            return False
        for attribute in self.lhs:
            if attribute not in tuple[self.relation_name]:
                return False
        return True

    def is_head_satisfied_by(self, tuple):
        if self.relation_name not in tuple:
            return False
        for attribute in self.rhs:
            if attribute not in tuple[self.relation_name]:
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

    def get_relation_name(self, attr: str) -> int:
        for i, attribute in enumerate(self.lhs):
            if attribute == attr:
                return i
        return -1

class EGD:
    def __init__(self, relation_name: str, lhs: List[Attribute], rhs: List[lambda _: bool], update: bool = False, expected_rhs: List[lambda _: _] = None):
        self.relation_name = relation_name
        self.lhs = lhs
        self.rhs = rhs
        self.update = update
        self.expected_rhs = expected_rhs
        self.applied_to = set()

    def is_satisfied_by(self, tuple):
        for attribute in self.lhs:
            if self.relation_name not in tuple or attribute not in tuple[self.relation_name]:
                return False
        return True
    
    def is_head_satisfied_by(self, tuple):
        for left_attribute, function in zip(self.lhs, self.rhs):
            if self.relation_name not in tuple:
                return False
            if not self.update:
                if function(tuple[self.relation_name]) == False:
                    return False
            else:
                if function(tuple[self.relation_name] != tuple[self.relation_name][left_attribute]):
                    return False
        return True
    
    def equalize(self, tuple):
        for attribute, function in zip(self.lhs, self.rhs):
            if not self.update:
                if function(tuple[self.relation_name]) == False:
                    tuple[self.relation_name][attribute] = None
            else:
                if function(tuple[self.relation_name]) != tuple[self.relation_name][attribute]:
                    tuple[self.relation_name][attribute] = function(tuple[self.relation_name])

    def mark_applied(self, tuple):
        self.applied_to.add(tuple)

    def is_applied_to(self, content: tuple):
        return content in self.applied_to

    def get_attribute_value(self, attr: Attribute, t: List[Tuple[str]]) -> str:
        for attribute in t:
            if attribute[0] == attr.name and attribute[1] == attr.relation_name:
                return attribute[2]
        return ""