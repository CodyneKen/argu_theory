import operator
from attacksGenerator import checkContradictionArg

class DefeatGenerator:

    def ShowRulesPreferences(self, rules):
        sorted_rules = []

        #sorting rules
        for rule in rules:
            if rule.defeasible:
                sorted_rules.append(rule)

        sorted_rules.sort(key=lambda a: a.indice, reverse = True)
        last_value = 0
        first = True

        for rule in sorted_rules:
            if first:
                last_value = rule.indice
                first = False
                print(rule.literal._name, "", end='')
            else:
                if last_value > rule.indice:
                    print(">", rule.literal._name, "", end='')
                    last_value = rule.indice
                else:
                    print(rule.literal._name, "", end='')
        
        print("")

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

    def getArgumentsPreferences(self, arguments, democratic, last_link):
        self.argumentsPreferences = []

        for arg in arguments:
            self.argumentsPreferences.sort(key=lambda a: a[1], reverse = True)

            if len(self.argumentsPreferences) == 0:
                if len(arg.defeasibleRules()) == 0:
                    self.argumentsPreferences.append((arg, 2))
                else:
                    self.argumentsPreferences.append((arg, 0))

            else:
                self.AddArgumentToPreferencesList(arg, democratic, last_link)

        self.argumentsPreferences.sort(key=lambda a: a[1], reverse = True)

    def DemocraticBetweenTwoRules(self, set_def_rule1, set_def_rule2):
        are_all_rules1_sup = True

        if len(set_def_rule1) == 0:
            return True
        
        for rule2 in set_def_rule2:
            are_all_rules1_sup = True
            
            for rule1 in set_def_rule1:
                if rule1.indice < rule2.indice:
                    are_all_rules1_sup = False

            if are_all_rules1_sup:
                return True

        return False

    def ElitistBetweenTwoRules(self, set_def_rule1, set_def_rule2):

        if len(set_def_rule1) == 0:
            return True
        
        if len(set_def_rule2) == 0:
            return False

        for rule1 in set_def_rule1:
            sup_equal = True

            for rule2 in set_def_rule2:
                if rule1.indice < rule2.indice:
                    sup_equal = False

            if sup_equal:
                return True
            
        return False

    def AddArgumentToPreferencesList(self, arg, democratic, last_link): # democratic is boolean
        last_value = 2
        cpt_arg = 0

        if len(arg.lastDefeasibleRules()) == 0:
            self.argumentsPreferences.append((arg, 2))
            return

        for arg2 in self.argumentsPreferences:
            cpt_arg += 1
            self.argumentsPreferences.sort(key=lambda a: a[1], reverse = True)
            dem_1 = 0
            dem_2 = 0

            if democratic:
                if last_link:
                    dem_1 = self.DemocraticBetweenTwoRules(arg.lastDefeasibleRules(), arg2[0].lastDefeasibleRules())
                    dem_2 = self.DemocraticBetweenTwoRules(arg2[0].lastDefeasibleRules(), arg.lastDefeasibleRules())
                else:
                    dem_1 = self.DemocraticBetweenTwoRules(arg.defeasibleRules(), arg2[0].defeasibleRules())
                    dem_2 = self.DemocraticBetweenTwoRules(arg2[0].defeasibleRules(), arg.defeasibleRules())
            else:
                if last_link:
                    dem_1 = self.ElitistBetweenTwoRules(arg.lastDefeasibleRules(), arg2[0].lastDefeasibleRules())
                    dem_2 = self.ElitistBetweenTwoRules(arg2[0].lastDefeasibleRules(), arg.lastDefeasibleRules())
                else:
                    dem_1 = self.ElitistBetweenTwoRules(arg.defeasibleRules(), arg2[0].defeasibleRules())
                    dem_2 = self.ElitistBetweenTwoRules(arg2[0].defeasibleRules(), arg.defeasibleRules())
            
            #print("#########", arg2[0].name)
            #for a in self.argumentsPreferences:
            #    print(a[0].name, "|", a[1])

            # si l'argument est préféré au sens démocratique on prend le score de celui avec qui on compare plus un
            if dem_1:
                if dem_2: #égal
                    self.argumentsPreferences.append((arg, arg2[1]))
                    #print(arg.name, "==", arg2[0].name)
                    return
                else: # strictement supérieur
                    self.argumentsPreferences.append((arg, (last_value + arg2[1]) / 2))
                    #print(arg.name, ">", arg2[0].name)
                    return
            
            else:
                #print(arg.name, "<", arg2[0].name)

                if cpt_arg == len(self.argumentsPreferences):
                    self.argumentsPreferences.append((arg, arg2[1] - 1))
                    return
                else:
                    last_value = arg2[1]

    def GenerateDefeats(self, undercuts, rebuts):
        self.defeats = set()

        for u in undercuts:
            self.defeats.add(u)

        for r in rebuts:
            sub_args = r.attacked.subArguments()
            run = True

            # subarguments of the attacked argument
            for arg in sub_args:

                if run and r.attacker._toprule.conclusion == ~arg._toprule.conclusion:

                    v1 = self.FindArgumentValueByName(r.attacker)
                    v2 = self.FindArgumentValueByName(arg)

                    if v1 >= v2:
                        self.defeats.add(r)
                        run = False
                        #break

            # also checking if conc(r.attacker) = ~(r.attacked)
            if run and r.attacker._toprule.conclusion == ~r.attacked._toprule.conclusion:
                v1 = self.FindArgumentValueByName(r.attacker)
                v2 = self.FindArgumentValueByName(r.attacked)

                if v1 >= v2:
                    self.defeats.add(r)
                    run = False

    def FindArgumentValueByName(self, arg):

        for tuple in self.argumentsPreferences:
            if tuple[0].name == arg.name:
                return tuple[1]