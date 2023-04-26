from typing import Dict, List, Tuple

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

    def is_satisfied_by(self, t: List[str]) -> bool:
        for a in self.lhs:
            if a.name not in t:
                return False
        return True

    def is_head_satisfied_by(self, t: List[str]) -> bool:
        for a in self.rhs:
            if a.name not in t:
                return False
        return True

    def mark_applied(self, t: List[str]) -> None:
        self.applied_to.add(tuple(t))

    def is_applied_to(self, t: List[str]) -> bool:
        return tuple(t) in self.applied_to

    def get_new_tuple(self, t: List[str], d: Dict[str, Relation]) -> List[str]:
        new_t = t.copy()
        for a in self.rhs:
            if a.name not in new_t:
                rel_name = self.get_relation_name(a.name)
                rel = d[rel_name]
                new_t += rel.tuples[0]
        return new_t

    def get_relation_name(self, attr_name: str) -> str:
        for a in self.lhs:
            if a.name == attr_name:
                return a.relation_name
        for a in self.rhs:
            if a.name == attr_name:
                return a.relation_name
        return None

class EGD:
    def __init__(self, lhs: List[Attribute], rhs: List[Attribute]):
        self.lhs = lhs
        self.rhs = rhs
        self.applied_to = set()

    def is_satisfied_by(self, t: List[str]) -> bool:
        lhs_values = [t[attr.name] for attr in self.lhs]
        rhs_values = [t[attr.name] for attr in self.rhs]
        return lhs_values == rhs_values

    def mark_applied(self, t: List[str]) -> None:
        self.applied_to.add(tuple(t))

    def is_applied_to(self, t: List[str]) -> bool:
        return tuple(t) in self.applied_to

    def equalize(self, t: List[str]) -> None:
        for a in self.rhs:
            t[a.name] = t[self.lhs[0].name]