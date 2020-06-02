import copy
from graphviz import Digraph


class PDAutomata:

    def __init__(self, start_state, final_states,  PDA):

        self.start_state = start_state
        self.final_states = final_states
        self.PDA = PDA

    def verify(self, current_state, current_stack, PDA, word):
        global ok

        print(current_state, current_stack, word)

        if word == "":
            if current_state in PDA:
                for x in PDA[current_state]:
                    if x[1] == "/":
                        if x[2] == "pop":
                            if current_stack[-1] == x[3]:
                                next_state = x[0]
                                next_stack = copy.deepcopy(current_stack[:-1])
                                self.verify(next_state, next_stack, PDA, word)
                        elif x[2] != "pop" and x[2] != "-":
                            if current_stack[-1] == x[3]:
                                next_state = x[0]
                                next_stack = copy.deepcopy(current_stack)
                                if len(x[2]) > 1:
                                    for i in range(len(x[2])):
                                        next_stack.append(x[2][i])
                                else:
                                    next_stack.append(x[2])
                                self.verify(next_state, next_stack, PDA, word)
                        elif x[2] == "-":
                            next_state = x[0]
                            next_stack = copy.deepcopy(current_stack)
                            self.verify(next_state, next_stack, PDA, word)

            if mod == 1:
                if current_state in final_states and current_stack != []:
                    ok = True
            elif mod == 2:
                if not current_stack:
                    ok = True
            elif mod == 3:
                if current_state in final_states and not current_stack:
                    ok = True

        else:
            if current_state in PDA:
                for x in PDA[current_state]:
                    if word[0] == x[1]:
                        if x[2] == "pop":
                            if current_stack[-1] == x[3]:
                                next_state = x[0]
                                next_stack = copy.deepcopy(current_stack[:-1])
                                self.verify(next_state, next_stack, PDA, word[1:])
                        elif x[2] != "pop" and x[2] != "-":
                            if current_stack[-1] == x[3]:
                                next_state = x[0]
                                next_stack = copy.deepcopy(current_stack)
                                if len(x[2]) > 1:
                                    for i in range(len(x[2])):
                                        next_stack.append(x[2][i])
                                else:
                                    next_stack.append(x[2])
                                self.verify(next_state, next_stack, PDA, word[1:])
                        elif x[2] == "-":
                            next_state = x[0]
                            next_stack = copy.deepcopy(current_stack)
                            self.verify(next_state, next_stack, PDA, word[1:])
                    elif word[0] == "/":
                        if x[2] == "pop":
                            if current_stack[-1] == x[3]:
                                next_state = x[0]
                                next_stack = copy.deepcopy(current_stack[:-1])
                                self.verify(next_state, next_stack, PDA, word)
                        elif x[2] != "pop" and x[2] != "-":
                            if current_stack[-1] == x[3]:
                                next_state = x[0]
                                next_stack = copy.deepcopy(current_stack)
                                if len(x[2]) > 1:
                                    for i in range(len(x[2])):
                                        next_stack.append(x[2][i])
                                else:
                                    next_stack.append(x[2])
                                self.verify(next_state, next_stack, PDA, word)
                        elif x[2] == "-":
                            next_state = x[0]
                            next_stack = copy.deepcopy(current_stack)
                            self.verify(next_state, next_stack, PDA, word)


def meniu():

    print("--- MODALITATE DE ACCEPTARE ---")
    print("1. Stare finala")
    print("2. Stiva vida")
    print("3. Stare finala + Stiva vida")


f = open("test3.txt")

meniu()
mod = int(input("Modalitate: "))

# Citire date + prelucrare

start_state = f.readline()[:-1]
final_states = f.readline().split()

current_state = start_state
current_stack = ['Z']

PDA = dict()

for x in f:
    aux = x.split()
    if aux[0] not in PDA.keys():
        PDA[aux[0]] = [[aux[1], aux[2], aux[3], aux[4]]]
    else:
        PDA[aux[0]].append([aux[1], aux[2], aux[3], aux[4]])

f.close()

# Afisare PDA

print("--- THE PDA ---")
print("The start state: ", start_state)
print("The final states: ", final_states)
print("The edges: ", PDA)

g = Digraph('DFA', filename='fsm.gv')
g.attr(rankdir='LR', size='10')
if start_state not in final_states:
    g.attr('node', shape='circle', fillcolor="green", style="filled")
    g.node(str(start_state))
else:
    g.attr('node', shape='doublecircle', fillcolor="green", style="filled")
    g.node(str(start_state))

g.attr('node', shape='doublecircle', fillcolor="red", style="filled")
for o in final_states:
    g.node(str(o))

g.attr('node', shape='circle', fillcolor="white", style="filled")
for x in PDA:
    if x not in final_states and x != start_state:
        g.node(str(x))

for x in PDA:
    for i in range(len(PDA[x])):
        g.edge(x, PDA[x][i][0], label=PDA[x][i][1] + " " + PDA[x][i][2] + " " + PDA[x][i][3], color="blue", style="filled")

g.view()

# Citire cuvant

nr_teste = int(input("Numarul de teste: "))

while nr_teste > 0:
    word = input("Word: ")
    ok = False

    x = PDAutomata(start_state, final_states, PDA)

    print("Current state | Current stack | Current word")

    x.verify(current_state, current_stack, PDA, word)

    if ok is True:
        print("ACCEPTED")
    else:
        print("NOT ACCEPTED")

    nr_teste -= 1
