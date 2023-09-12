import sys
import heapq

args = sys.argv[1:]
filename = args[0]


# definition of state class
class state:
    def __init__(self, cond, heuristic):
        self.cond = cond
        self.parent = None
        self.heuristic = heuristic

    def __lt__(self, other):
        return self.heuristic < other.heuristic

    def __eq__(self, other):
        return self.cond == other.cond

    def __str__(self):
        return str(self.cond) + " " + str(self.heuristic)


# grades a state and assigns heuristic value
def gradestate(state):
    return 1


# function that adds state to the hash table of known states
def addstate(state, table):
    statestr = state.cond[0]
    for i in state.cond[1:]:
        statestr += "-" + i
    table[statestr] = 1


# function that checks whether state is in the hash table of known states
def checkstate(state, table):
    statestr = state.cond[0]
    for i in state.cond[1:]:
        statestr += "-" + i
    return table.get(statestr) is not None


# generates all possible states from current state
def genstates(parent_state):
    states = []
    for i in range(0, len(parent_state.cond)):
        if parent_state.cond[i] == "":
            continue
        for j in range(1, len(parent_state.cond)):
            newcond = parent_state.cond.copy()
            lastdig = newcond[i][-1]
            newcond[i] = newcond[i][0:-1]
            newcond[(i + j) % len(parent_state.cond)] += lastdig
            newstate = state(newcond, gradestate(newcond))
            newstate.parent = parent_state
            states.append(newstate)
    return states


with open("probs/" + filename, "r") as f:
    # read basic file info
    lines = f.readlines()
    col_num, block_num, move_num = lines[0].strip().split()
    col_num = int(col_num)
    block_num = int(block_num)
    move_num = int(move_num)

    # read initial state and goal state from file
    cond = []
    line_num = 2
    for i in range(0, col_num):
        cond.append(lines[line_num + i].strip())
    line_num += int(col_num) + 1
    goal = []
    for i in range(0, col_num):
        goal.append(lines[line_num + i].strip())

    # debug printouts
    print("state:", cond)
    print("goal:", goal)
    ancestor_state = state(cond, gradestate(cond))
    states = genstates(ancestor_state)
    known_states = dict()
    addstate(ancestor_state, known_states)
    heapq.heapify(states)
    while len(states) > 0:
        best = heapq.heappop(states)
        if best.cond == goal:
            print("goal reached\nFinal state:", best.cond)
            pathtogoal = []
            while best.parent is not None:
                pathtogoal.append(best.cond)
                best = best.parent
            print("path to goal:")
            print(ancestor_state.cond)
            for i in pathtogoal[::-1]:
                print(i)
            print("number of moves:", len(pathtogoal))
            break
        else:
            newstates = genstates(best)
            for i in newstates:
                if not checkstate(i, known_states):
                    heapq.heappush(states, i)
                    addstate(i, known_states)
