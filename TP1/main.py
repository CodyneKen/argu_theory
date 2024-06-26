from rule import *
from argumentGenerator import *
from attacksGenerator import *
from defeatsGenerator import *
from rankArgument import *

rules = set()
a = Literal('a', True)
b = Literal('b', True)
c = Literal('c', True)
d = Literal('d', True)
e = Literal('e', True)
nc = Literal('c', False)
nd = Literal('d', False)

r1 = Rule(set(), a, False, "r1")
r2 = Rule({b, d}, c, False, "r2")
r3 = Rule({nc}, d, False, "r3")

r4 = Rule({a}, nd, True, "r4", 0)
r5 = Rule(set(), b, True, "r5", 1)
r6 = Rule(set(), nc, True, "r6", 1)
r7 = Rule(set(), d, True, "r7", 0)
r8 = Rule({c}, e, True, "r8", 0)
r9 = Rule({nc}, ~(r4), True, "r9", 0)

rules.add(r1)
rules.add(r2)
rules.add(r3)
rules.add(r4)
rules.add(r5)
rules.add(r6)
rules.add(r7)
rules.add(r8)
rules.add(r9)


arguments = generateArguments(rules)

for arg in arguments:
    print(arg, "|", arg._toprule.literal._name)

print("taille:", len(arguments))


######## Generating attacks ########
print("\n--- Attack Generator ---")
undercuts = generateUndercutsAttack(arguments)
rebuts = generateRebutsAttacks(arguments)
print("Rebuts - (Attaquant, Attaqué) - Taille: ", len(rebuts))
#for rebut in rebuts:
#    print("(", rebut.attacker, ", ", rebut.attacked, ")", sep="")

print("UNDERCUTS- (Attaquant, Attaqué) - Taille: ", len(undercuts))


######## Generating defeats ########
print("\n--- Defeats generator ---")
dg = DefeatGenerator()
#dg.showPreferences(dg.rules_preferences)
dg.getArgumentsPreferences(arguments, False, True)

print("nb arg:", len(dg.argumentsPreferences))

dg.GenerateDefeats(undercuts, rebuts)

#for a in dg.defeats:
#    print("(", a.attacker.name, ", ", a.attacked.name, ")", sep="")

dg.ShowRulesPreferences(rules)
dg.ShowArgumentsPreferences()
print("\nNb defeats:", len(dg.defeats))

### Rank Argument - burden-based-semantics
print("### Rank Argument ###")
dictArgWithRanks = getDictArgsWithRanks(arguments, dg.defeats, 0.5)
so = dict( sorted(dictArgWithRanks.items(), key=operator.itemgetter(1), reverse=True))
print(dg.showPreferencesString(so))
#print("nb arg after preferences:", len(dg.finalArgumentsPreferences))