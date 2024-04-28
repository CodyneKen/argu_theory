import sys
import os
# To allow import from outside folder (yes it's ugly and hacky)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from rule import *
from argument import *


class Attack:
    counter = 1
    attacker: Argument
    attacked: Argument

    def __init__(self, attacker, attacked):
        self.name = "attack" + str(Attack.counter)
        Attack.counter += 1
        self.attacker = attacker
        self.attacked = attacked

    @staticmethod
    def reset_counter():
        Attack.counter = 1

    def __str__(self):
        return f"""att({self.attacker.name}, {self.attacked.name})"""

    def __hash__(self):
        # Not sure if modulo is smart here
        # Might have collision (insanely low chance)
        hashish = self.attacker.__hash__() % self.attacked.__hash__()
        return hash(hashish)
