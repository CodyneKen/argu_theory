from rule import *
from argument import *
from attacks import *


def checkCInDefeasible(conclusion, defeasibles):
    for rule in defeasibles:
        if conclusion == rule.literal:
            return True
    return False


# Retourne les couples d'arguments attaquant (un seul considéré)/attaqué (plusieurs possibles) si c'est le cas
def checkAttackDefeasible(argument, arguments):
    undercuts = set()
    for arg in arguments:
        if (checkCInDefeasible(argument._toprule.conclusion, arg.defeasibleRules())):
            undercuts.add((argument, arg))
    return undercuts


def generateUndercuts(arguments):
    undercuts = set()
    for arg in arguments:
        temp = checkAttackDefeasible(arg, arguments)
        undercuts.update(temp)
    return undercuts


def generateUndercutsAttack(arguments):
    undercut_attacks = set()
    undercuts = generateUndercuts(arguments)
    for arg in undercuts:
        undercut_attacks.add(Attack(arg[0], arg[1]))
    return undercut_attacks


# Peut-être mettre un appel récursif
def checkContradictionAllSubargs(conclusion, allSubArguments):
    for arg in allSubArguments:
        if (conclusion == ~(arg._toprule.conclusion)):
            return True
    return False


def checkContradictionArg(conclusion, arg):
    if (conclusion == ~(arg._toprule.conclusion)):
        return True
    return checkContradictionAllSubargs(conclusion, arg.subArguments())


def checkRebuts(argument, arguments):
    rebuts = set()
    for arg in arguments:
        # if (argument != arg):
        if (checkContradictionArg(argument._toprule.conclusion, arg)):
            rebuts.add((argument, arg))

    return rebuts


def generateRebuts(arguments):
    rebuts = set()
    for arg in arguments:
        temp = checkRebuts(arg, arguments)
        rebuts.update(temp)
    return rebuts


def generateRebutsAttacks(arguments):
    rebut_attacks = set()
    rebuts = generateRebuts(arguments)
    for arg in rebuts:
        rebut_attacks.add(Attack(arg[0], arg[1]))
    return rebut_attacks
