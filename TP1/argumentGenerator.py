from rule import *
from argument import *
import itertools


def generateContrapos(rules):
    contrapos = set()
    contrapos.update(rules)

    for rule in rules:
        contrapos.update(rule.gen_contrapo())

    return contrapos


def generateArgumentsWithoutPremises(rules):
    arguments = set()

    for rule in rules:
        print(rule)
        if not rule.premises:
            arguments.add(Argument(rule))
    
    print("#######")
    return arguments


#ne fonctionne pas si 3 lites d'arguments
def generateAllArgumentsOfAllPremises(rule, arguments):

    allArguments = []
    finalArgument = set()

    for premise in rule.premises:
        arguments_for_this_premise = {a for a in arguments if a._toprule.conclusion == premise}
        allArguments.append(arguments_for_this_premise)

    for subargs in itertools.product(*allArguments):
        new_arg = Argument(rule)
        new_arg._subarguments.update(subargs)
        finalArgument.add(new_arg)

    return finalArgument


def isArgumentAlreadyInArgumentList(argument, arguments):

    for arg in arguments:
        if argument == arg:
            return True
        
    return False


def generateArguments(rules):
    rules_contr = generateContrapos(rules)
    arguments = generateArgumentsWithoutPremises(rules_contr)

    added_arg = True
    length_arg = 0

    while added_arg:
        added_arg = False

        for rule in rules_contr:
            arguments_of_this_rule = generateAllArgumentsOfAllPremises(rule, arguments)
            
            for arg in arguments_of_this_rule:
                if len(arg._subarguments) == len(rule.premises):
                    if not isArgumentAlreadyInArgumentList(arg, arguments):
                        arguments.add(arg)

        if length_arg != len(arguments):
            added_arg = True
            length_arg = len(arguments)

    return arguments

