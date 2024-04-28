from rule import *


class Argument:
    counter = 1

    def __init__(self, toprule):
        self.name = "a" + str(Argument.counter)
        Argument.counter += 1
        self._subarguments = set()
        self._toprule = toprule  # Dernière règle qui a été appliquée

    @staticmethod
    def reset_counter():
        Argument.counter = 1

    def __str__(self):
        if (self._toprule.defeasible):
            str = f"""[{self.name}]: {", ".join(f"{sub.name}" for ind, sub in enumerate(self._subarguments))} => {self._toprule.conclusion}"""
        else:
            str = f"""[{self.name}]: {", ".join(f"{sub.name}" for ind, sub in enumerate(self._subarguments))} -> {self._toprule.conclusion}"""
        return str

    def __eq__(self, other) -> bool:
        return self._subarguments == other._subarguments and self._toprule == other._toprule

    def __hash__(self):
        return hash(self.name)

    # Write a method to access the set of all defeasible rules of an argument
    def defeasibleRules(self):
        retSet = set()
        if self._toprule.defeasible:
            retSet.add(self._toprule)
        for suba in self._subarguments:
            retSet.update(suba.defeasibleRules())

        return retSet

    # Write a method to access the set of last defeasible rules of an argument
    # We understand it as the most toplevel set of defeasible rules starting from argument
    def lastDefeasibleRules(self):
        retSet = set()
        if self._toprule.defeasible:
            retSet.add(self._toprule)
            return retSet
        # if we didn't find any defeasible rule, we go to level n-1
        else:
            for suba in self._subarguments:
                retSet.update(suba.lastDefeasibleRules())

        return retSet

    # Write a method to access the set of all subarguments of an argument
    def subArguments(self):
        return self._subarguments.union(*(suba.subArguments() for suba in self._subarguments))
