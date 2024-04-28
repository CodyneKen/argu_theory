import operator
from attacksGenerator import checkContradictionArg

class DefeatGenerator:

    def __init__(self):
        self.rules_preferences = {
            "r5": 1,
            "r6": 1,
            "r4": 0,
            "r7": 0,
            "r8": 0,
            "r9": 0
        }

    def showPreferences(self, dict):
        last_value = 0
        begin = True

        for key in dict:
            if begin:
                begin = False
                last_value = dict[key]

            if dict[key] < last_value:
                last_value = dict[key]
                print('> ', end="")
            
            print(key, "", end="")
        print("")

   # Should be static
    def showPreferencesString(self, dict):
        last_value = 0
        begin = True
        output = ""
        for key in dict:
            if begin:
                begin = False
                last_value = dict[key]

            if dict[key] < last_value:
                last_value = dict[key]
                output += '> '
            output += key + " "
        return output

    def ShowArgumentsPreferences(self):
        last_score = 0
        first = True

        for tuple in self.argumentsPreferences:
            if first:
                first = False
                last_score = tuple[1]
                print(tuple[0].name, "", end='')

            elif tuple[1] != last_score:
                print(">", tuple[0].name, "", end='')
                last_score = tuple[1]
            else:
                print(tuple[0].name, "", end='')


    def getArgumentsPreferences(self, arguments):
        self.argumentsPreferences = []

        for arg in arguments:

            if len(self.argumentsPreferences) == 0:
                if len(arg.lastDefeasibleRules()) == 0:
                    self.argumentsPreferences.append((arg, 2))
                else:
                    self.argumentsPreferences.append((arg, 0))

            else:
                self.AddArgumentToPreferencesList(arg)  

        self.argumentsPreferences.sort(key=lambda a: a[1], reverse = True)


    def DemocraticBetweenTwoRules(self, set_def_rule1, set_def_rule2):
        are_all_rules1_sup = True

        if len(set_def_rule1) == 0:
            return True
        
        for rule2 in set_def_rule2:
            are_all_rules1_sup = True
            
            for rule1 in set_def_rule1:
                if self.rules_preferences[rule1.literal._name] < self.rules_preferences[rule2.literal._name]:
                    are_all_rules1_sup = False

            if are_all_rules1_sup:
                return True

        return False

    def AddArgumentToPreferencesList(self, arg):
        last_value = 2
        cpt_arg = 0

        if len(arg.lastDefeasibleRules()) == 0:
            self.argumentsPreferences.append((arg, 2))
            return

        for arg2 in self.argumentsPreferences:
            cpt_arg += 1
            self.argumentsPreferences.sort(key=lambda a: a[1], reverse = True)
            print("#########")
            for a in self.argumentsPreferences:
                print(a[0].name, "|", a[1])
            dem_1 = self.DemocraticBetweenTwoRules(arg.lastDefeasibleRules(), arg2[0].lastDefeasibleRules())
            dem_2 = self.DemocraticBetweenTwoRules(arg2[0].lastDefeasibleRules(), arg.lastDefeasibleRules())
            
            # si l'argument est préféré au sens démocratique on prend le score de celui avec qui on compare plus un
            if dem_1:
                if dem_2: #égal
                    self.argumentsPreferences.append((arg, arg2[1]))
                    print(arg.name, "==", arg2[0].name)
                    return
                else: # strictement supérieur
                    self.argumentsPreferences.append((arg, (last_value + arg2[1]) / 2))
                    print(arg.name, ">", arg2[0].name)
                    return
            
            else:
                if cpt_arg == len(self.argumentsPreferences):
                    self.argumentsPreferences.append((arg, last_value -1))
                else:
                    print(arg.name, "<", arg2[0].name)
                    last_value = arg2[1]

    
    def GenerateDefeats(self, undercuts, rebuts):
        self.defeats = []

        for u in undercuts:
            self.defeats.append(u)

        for r in rebuts:
            sub_args = r.attacked.subArguments()

            for arg in sub_args:

                if r.attacker._toprule.conclusion == ~arg._toprule.conclusion:

                    v1 = self.FindArgumentValueByName(r.attacker)
                    v2 = self.FindArgumentValueByName(arg)

                    if v1 >= v2:
                        self.defeats.append(r)
                        break
                        

    def FindArgumentValueByName(self, arg):

        for tuple in self.argumentsPreferences:
            if tuple[0].name == arg.name:
                return tuple[1]