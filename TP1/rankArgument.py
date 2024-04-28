import sys
import os
# To allow import from outside folder (yes it's ugly and hacky)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


import operator
from typing import List, Set, Tuple, Dict
from defeatsGenerator import *
from argument import *
from attacks import *

"""
Compute the ranking between arguments using the burden-based-semantics.
Output of computeBurdenValuesArguments is a dict, where a key is the name of the argument,
and the key's value is a list with all its Burden numbers.
Bur(a1) = <1, 2, ...> <=> "a1": [1, 2, ...] 
"""

def getAttackers(argument: Argument, attacks: Set[Attack]):
    attackers = []
    for attack in attacks:
        if attack.attacked == argument:
            attackers.append(attack.attacker)
    return attackers

def computeBurden(arg: Argument, burdens: Dict, attackers: List[Argument], epsilon, curIndex):
    if len(burdens[arg.name]) >= 2:
        if abs(burdens[arg.name][-1] - burdens[arg.name][-2]) - epsilon <= 0:
            burdens[arg.name].insert(curIndex, burdens[arg.name][curIndex-1]) # Pas eu de changement pour cet argument
            return False
        else:
            # Il a forcément au moins un attaquant, car sinon la condition du haut aurait été vraie dès curIndex == 2
            total_sum = 1 + round(sum(1/(burdens[attacker.name][curIndex - 1]) for attacker in attackers), 10) # curIndex >= 2
            burdens[arg.name].insert(curIndex, total_sum)
            return True
            
    else: # On calcule la deuxième burdenValue, sans tester la convergence, donc curIndex == 1
        if not attackers: # pas d'attaquants
            burdens[arg.name].insert(1, 1) # et curIndex vaut forcément 1
        else:
            total_sum = 1 + round(sum(1/(burdens[attacker.name][0]) for attacker in attackers), 10)
            burdens[arg.name].insert(1, total_sum)
        return True
    
def computeAllRankLargeur(arguments: Set[Argument], burdens: Dict, attackers: List[Argument], epsilon):
    curIndex = 1 # car pour l'index 0, burdenValue vaut déjà 1
    while True: # On boucle tant qu'il y a eu au moins une modification
        all_false = True
        for arg in arguments:
            argAttackers = attackers[arg.name]
            if computeBurden(arg, burdens, argAttackers, epsilon, curIndex):
                all_false = False # la dernière burdenValue d'un des arguments a changé
        if all_false:
            break
        curIndex += 1
    
def computeBurdenValuesArguments(arguments: Set[Argument], attacks: Set[Attack], epsilon):
    burdens = dict()
    attackers = dict()
    # Initialize burdens & attackers dictionary
    for argument in arguments:
        burdens.update({argument.name: [1]})
        attackersList = getAttackers(argument, attacks)
        attackers.update({argument.name: attackersList})
        
    computeAllRankLargeur(arguments=arguments, burdens=burdens, attackers=attackers, epsilon=epsilon)
    return burdens, attackers


def lexicographicalComparison(burdenA: List, burdenB: List): # Fonction qui retourne vraie si burdenA est meilleure que burdenB
    for i in range(len(burdenA)):
        if (burdenA[i] == burdenB[i]):
            continue
        elif (burdenA[i] < burdenB[i]): # A meilleur que B
            return True
        elif (burdenB[i] < burdenA[i]): # B meilleur que A
            return False

def triInsertion(listToSort: List, burdens: Dict):
    for i in range(len(listToSort)):
        key = listToSort[i]
        burdenOfKey = burdens[key]
        j = i-1
        while j >= 0 and burdens[listToSort[j]] > burdenOfKey:
            listToSort[j+1] = listToSort[j] # decalage
            j = j-1
        listToSort[j+1] = key


# Bonne version
# Fonction qui prend dict non trié, et qui regarde, si le suivant et le précédent sont exactement les mêmes, alors ils ont le même rang, sinon ils n'ont pas le même rang
def rankFromBurdens2(burdens: Dict):
    sortedKeysList = [] # contient uniquement les clé
    for burden in burdens:
        sortedKeysList.append(burden)
    triInsertion(sortedKeysList, burdens)
    sortedKeysListReversed = list(reversed(sortedKeysList))
    rank = -1
    result = {}
    previousValue = None
    for key in sortedKeysListReversed:
        value = burdens[key] # [1, 1, 1, 1, 1, 1, 1, 1, 1]
        if value != previousValue:
            rank += 1
        result[key] = rank
        previousValue = value
    return result

def getDictArgsWithRanks(arguments: Set[Argument], attacks: Set[Attack], epsilon):
    burdens, _ = computeBurdenValuesArguments(arguments, attacks, epsilon)
    # print(burdens)
    dictArgsWithRanks = rankFromBurdens2(burdens)
    return dictArgsWithRanks