from rule import *
from argumentGenerator import *
from attacksGenerator import *
from defeatsGenerator import *
from rankArgument import *
import operator

rules = set()
a = Literal('a', True)
b = Literal('b', True)
c = Literal('c', True)
d = Literal('d', True)
e = Literal('e', True)
nc = Literal('c', False)
nd = Literal('d', False)

r1 = Rule(set(), a, False)
r3 = Rule({b, d}, c, False)
r5 = Rule({nc}, d, False)

r2 = Rule({a}, nd, True)
r4 = Rule(set(), b, True)
r6 = Rule(set(), nc, True)
r7 = Rule(set(), d, True)
r8 = Rule({c}, e, True)
r9 = Rule({nc}, ~(r2), True)
rules.add(r1)
rules.add(r2)
rules.add(r3)
rules.add(r4)
rules.add(r5)
rules.add(r6)
rules.add(r7)
rules.add(r8)
rules.add(r9)

preferences = {
    r4: [r2, r7, r8, r9],
    r6: [r2, r7, r8, r9]
}

arguments = generateArguments(rules)

for arg in arguments:
    print(arg)

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
dg.showPreferences(dg.rules_preferences)
dg.getArgumentsPreferences(arguments)

print("nb arg:", len(dg.argumentsPreferences))


dg.GenerateDefeats(undercuts, rebuts)

#for a in dg.defeats:
#    print("(", a[0].name, ", ", a[1].name, ")", sep="")

dg.ShowArgumentsPreferences()
print("Nb defeats:", len(dg.defeats))

### Rank Argument - burden-based-semantics
print("### Rank Argument ###")
#dictArgWithRanks = getDictArgsWithRanks(arguments, rebuts, 0.5)
#so = dict( sorted(dictArgWithRanks.items(), key=operator.itemgetter(1), reverse=True))
#print(dg.showPreferencesString(so))
#print("nb arg after preferences:", len(dg.finalArgumentsPreferences))