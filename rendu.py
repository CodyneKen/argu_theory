from TP1.rule import *
from TP1.argumentGenerator import *
from TP1.attacksGenerator import *
from TP1.defeatsGenerator import *
import operator


# For debugging
if __name__ == '__main__':
    # Open the KB.txt file in read mode
    with open('KBs/KB.txt', 'r') as file:
        # Create a set to store the rules
        rules = set()
        # Read each line of the file
        for line in file:
            # Parse the rule and add it to the set
            rules.add(parse_rule(line))

        # Is going to be calculated again in generateArguments, just for keeping track
        extended_rules = generateContrapos(rules)

        print("nb_rules:", len(rules))
        print("nb_extended_rules:", len(extended_rules))
        # Generate arguments based on the rules
        # GenerateArguments prints the rules generated somehow
        arguments = generateArguments(rules)
        # Print the arguments
        for arg in arguments:
            print(arg)

        print("nb_arguments:", len(arguments))
