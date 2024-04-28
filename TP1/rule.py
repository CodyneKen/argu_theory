import sys
import os

# To allow import from outside folder (yes it's ugly and hacky)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from literal import Literal


class Rule:
    counter = 0

    # Si pas de premises, alors p = []
    def __init__(self, p, c, d):
        self.premises = p  # array
        self.conclusion = c
        self.defeasible = d  # boolean, False if not defeasible
        self.literal = Literal("r" + str(Rule.counter), True)
        Rule.counter += 1

    @staticmethod
    def reset_counter():
        Rule.counter = 0

    def __str__(self) -> str:
        if len(self.premises) != 0:
            if not (self.defeasible):
                str = f"""[{self.literal}]: {", ".join(f"{premise}" for ind, premise in enumerate(self.premises))} -> {self.conclusion}"""
            else:
                str = f"""[{self.literal}]: {", ".join(f"{premise}" for ind, premise in enumerate(self.premises))} => {self.conclusion}"""
        else:
            if not (self.defeasible):
                str = f"""[{self.literal}]: -> {self.conclusion}"""
            else:
                str = f"""[{self.literal}]: => {self.conclusion}"""
        return str

    def __eq__(self, other):
        return self.premises == other.premises and self.conclusion == other.conclusion

    def __invert__(self):
        if self.defeasible:
            return self.literal
        return ~(self.literal)

    def __hash__(self):
        return hash((self.literal._name, self.literal._verite))  # Hash le nom ou le nom+1 si la negation

    def gen_contrapo(self):
        # Si stricte et a des premises
        if not (self.defeasible) and len(self.premises) != 0:
            contrapo_rules = set()
            for premise in self.premises:
                new_premises = set()
                new_premises.update(self.premises.copy())
                new_premises.remove(premise)
                new_premises.add(~self.conclusion)
                contrapo_rules.add(Rule(new_premises, ~(premise), False))
            return contrapo_rules
        return set()
