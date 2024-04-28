import math
from datetime import time

from flask import Flask, render_template, request
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from TP1.rankArgument import *
from TP1.rule import *
from TP1.argumentGenerator import *
from TP1.attacksGenerator import *
from TP1.defeatsGenerator import *
import operator

app = Flask(__name__)


def separate_rules(rule):
    return rule.split(';')


def str_to_rule(rule_name, literals, strict, conclusion, indice=None):
    literal_set = set()
    for literal in literals:
        # Determine whether the literal is negated
        is_negated = literal.startswith('!')
        # Create a Literal object and add it to the set
        literal_set.add(Literal(literal[1:] if is_negated else literal, not is_negated))

    # Check if the conclusion starts with '!'
    if conclusion.startswith('!'):
        # If it does, create a Literal object with the conclusion (excluding the '!') and False
        conclusion_literal = Literal(conclusion[1:], False)
    else:
        # If it doesn't, create a Literal object with the conclusion and True
        conclusion_literal = Literal(conclusion, True)

    # Create a Rule object with the set of literals, the conclusion literal, and whether the rule is strict
    rule = Rule(literal_set, conclusion_literal, not strict, indice)
    return rule


def parse_rule2(line):
    # Extract rule name between brackets (removing it from the line)
    rule_name = line[line.find('[') + 1:line.find(']')]
    line = line.replace('[' + rule_name + ']', '')
    # split the remainder into whats on the left and right of the arrow, which can be -> or =>
    strict = '->' in line
    parts = line.strip().split('->' if strict else '=>')
    if len(parts) != 2:
        print("Error: Rule not well formatted")
        return None
    # split the left part into literals
    literals = parts[0].split(',') if parts[0] else []
    # split the right part into a single literal
    conclusion = parts[1]
    return str_to_rule(rule_name, literals, strict, conclusion)

# TODO INVERSé les rules strict/defeasible, a switch
def parse_rule(line):
    # Remove whitespace and split the line into parts
    parts = line.strip().split(' ')
    # The first part is the rule name
    rule_name = parts[0]
    # The rest is the rule body and conclusion
    rule_body_and_conclusion = parts[1]
    # Split the rest into literals and conclusion
    literals_and_conclusion = rule_body_and_conclusion.split('->' if '->' in rule_body_and_conclusion else '=>')
    # The first part is the rule body
    rule_body = literals_and_conclusion[0]
    # The second part is the conclusion
    conclusion = literals_and_conclusion[1]
    # Split the rule body into literals
    literals = rule_body.split(',') if rule_body else []
    # Determine whether the rule is strict or defeasible
    is_strict = '->' in rule_body_and_conclusion
    # Create a set of literals

    if len(literals_and_conclusion) > 2:
        indice = literals_and_conclusion[2]
        rule = str_to_rule(rule_name, literals, not is_strict, conclusion, indice)

    rule = str_to_rule(rule_name, literals, is_strict, conclusion)

    return rule


def gen_attack_graph(attack_space, name):
    G = nx.DiGraph()
    G.clear()  # Clear the graph
    # idNode = 0
    for a in attack_space:
        print("in gen_attack_graph", a.attacker.name, a.attacked.name)
        if a.attacker.name not in G:
            print("in gen_attack_graph added node R", a.attacker.name)
            G.add_node(a.attacker.name)
        if a.attacked.name not in G:
            print("in gen_attack_graph added node D", a.attacked.name)
            G.add_node(a.attacked.name)
        G.add_edge(a.attacker.name, a.attacked.name)
        # G.add_edge(idNode, idNode)

    if G.order() != 0:
        # Faire varier le factor si résultat trop dense/sparse, a voir si on
        # peut autoriser l'utilisateur à choisir
        factor = 7
        k_val = factor / math.sqrt(G.order())
    else:
        k_val = 1
    # https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html
    pos = nx.spring_layout(G, k=k_val)
    # https: // networkx.org / documentation / stable / reference / generated / networkx.drawing.layout.spectral_layout.html
    # pos = nx.spectral_layout(G)

    plt.clf()
    nx.draw_networkx_nodes(G, pos)
    # Specify to use node names as labels
    nx.draw_networkx_labels(G, pos)
    # Pick arrow style for graph
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=10)

    # g_name = "static/images/" + name + "_attack_graph.png"
    if (name == "rebuts"):
        g_name = "static/images/rebuts_attack_graph.png"
    else:
        g_name = "static/images/undercuts_attack_graph.png"
    plt.savefig(g_name, format="PNG", bbox_inches='tight', pad_inches=-0.1)


@app.route('/', methods=['GET', 'POST'])
def home():
    display_data = {}
    if request.method == 'POST':
        rule = request.form.get('rule')
        Rule.reset_counter()
        print("Rule counter:", Rule.counter)
        rule_space = set()
        rule_array = separate_rules(rule)
        for r in rule_array:
            rule_space.add(parse_rule(r))

        # Flask input :
        print('Rule (separated by ; for several):', rule)
        for r in rule_space:
            print(r)

        print("Rule space - Taille: ", len(rule_space))

        extended_rule_space = set()
        extended_rule_space = generateContrapos(rule_space)
        for r in extended_rule_space:
            print(r)

        print("Extended rule space - Taille: ", len(extended_rule_space))
        Argument.reset_counter()
        arguments = generateArguments(rule_space)

        Attack.reset_counter()
        attacks_rebuts_space = set()
        print("Arguments - Taille: ", len(arguments))
        attacks_rebuts_space = generateRebutsAttacks(arguments)
        print("Rebuts - (Attaquant, Attaqué) - Taille: ", len(attacks_rebuts_space))
        # for at in attacks_rebuts_space:
        #     print(at)

        attacks_undercuts_space = set()
        print("Arguments - Taille: ", len(arguments))
        attacks_undercuts_space = generateUndercutsAttack(arguments)
        print("Undercuts - (Attaquant, Attaqué) - Taille: ", len(attacks_undercuts_space))
        # for at in attacks_undercuts_space:
        #     print(at)

        # gen_attack_graph(attacks_rebuts_space, "rebuts")
        # gen_attack_graph(attacks_undercuts_space, "undercuts")

        # Defeat are successful attacks
        # filtered_attacks = defeats - all_attacks
        # Passe 94 -> 77

        rebuts = generateRebuts(arguments)
        ### Rank Argument - burden-based-semantics
        print("### Rank Argument ###")
        dg = DefeatGenerator()
        dictArgWithRanks = getDictArgsWithRanks(arguments, rebuts, 0.5)
        so = dict(sorted(dictArgWithRanks.items(), key=operator.itemgetter(1), reverse=True))
        print(dg.showPreferencesString(so))

        # Display arguments, rules
        # TODO Make the display graphical
        display_data = {
            # SET SPACES
            'rules': rule_space,
            'arguments': arguments,
            'extended_rule_space': extended_rule_space,
            'rebuts_space': attacks_rebuts_space,
            'undercuts_space': attacks_undercuts_space,
            'ranking_burden': dg.showPreferencesString(so),
            # LENGTHS (can't be calculated in page)
            'extended_rule_length': len(extended_rule_space),
            'rule_length': len(rule_space),
            'arguments_length': len(arguments),
            'rebuts_length': len(attacks_rebuts_space),
            'undercuts_length': len(attacks_undercuts_space),

        }
        return render_template('index.html', data=display_data, current_time=time())

    return render_template('index.html', data=display_data, current_time=time())


if __name__ == '__main__':
    app.run(debug=True)
