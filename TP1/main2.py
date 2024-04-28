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
nc = Literal('c', False)
nb = Literal('b', False)
na = Literal('a', False)


r1 = Rule(set(), c, False)
r2 = Rule({d}, nb, False)

r3 = Rule(set(), a, True)
r4 = Rule(set(), b, True)
r5 = Rule({a, b}, nc, True)
r6 = Rule({c}, d, True)
r7 = Rule({d}, na, True)
r8 = Rule({nb}, ~(r6), True)


rules.add(r1)
rules.add(r2)
rules.add(r3)
rules.add(r4)
rules.add(r5)
rules.add(r6)
rules.add(r7)
rules.add(r8)


arguments = generateArguments(rules)

for arg in arguments:
    print(arg)

print("taille:", len(arguments))


######## Generating attacks ########
print("\n--- Attack Generator ---")
undercuts = generateUndercutsAttack(arguments)
rebuts = generateRebutsAttacks(arguments)
print("Rebuts - (Attaquant, Attaqué) - Taille: ", len(rebuts))
for rebut in rebuts:
    print("(", rebut.attacker.name, ", ", rebut.attacked.name, ")", sep="")

print("UNDERCUTS- (Attaquant, Attaqué) - Taille: ", len(undercuts))
for u in undercuts:
    print("(", u.attacker.name, ", ", u.attacked.name, ")", sep="")

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
print("\nNb defeats:", len(dg.defeats))

