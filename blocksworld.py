import sys
import heapq
import time

args = sys.argv[1:]
filename = args[0]

goal = []
goalMap = dict()


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
def H0(state):
    h = 0
    for i in range(0, len(state)):
        for j in range(0, len(state[i])):
            if i != goalMap[state[i][j]][0]:
                h += 1
            if j != goalMap[state[i][j]][1]:
                h += abs(j - goalMap[state[i][j]][1])
    return h


# grades a state and assigns heuristic value
def H1(state):
    h = 0
    for i in range(0, len(state)):
        for j in range(0, len(state[i])):
            if i != goalMap[state[i][j]][0]:
                h += 1 + len(state[i]) - j
    return h


gradestate = H0
# if len(args) > 1 and args[2] == "-H":
#     gradestate = fun(args[3])


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
            newstate = state(newcond, 0)
            newstate.parent = parent_state
            states.append(newstate)
    return states


with open("probs/" + filename, "r") as f:
    # read basic file info
    t0 = time.time()
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
    for i in range(0, col_num):
        goal.append(lines[line_num + i].strip())
    for i in range(0, len(goal)):
        for j in range(0, len(goal[i])):
            goalMap[goal[i][j]] = [i, j]

    # debug printouts
    print("State:", cond)
    print("Goal:", goal)
    print("Using heuristic:", gradestate)
    ancestor_state = state(cond, gradestate(cond))
    states = genstates(ancestor_state)
    iters = 0
    MAX_ITERS = 1000000
    for i in states:
        i.heuristic = gradestate(i.cond)
    known_states = dict()
    addstate(ancestor_state, known_states)
    heapq.heapify(states)
    while len(states) > 0:
        if iters >= MAX_ITERS:
            print("max iters (%g) reached" % MAX_ITERS)
            print("current state:", best.cond)
            break
        iters += 1
        best = heapq.heappop(states)
        # best = states.pop(0)
        if best.cond == goal:
            print("\033[34mGoal reached!\n\033[0mFinal state:", best.cond)
            pathtogoal = []
            while best.parent is not None:
                pathtogoal.append(best.cond)
                best = best.parent
            print("path to goal:")
            print(ancestor_state.cond)
            for i in pathtogoal[::-1]:
                print(i)
            print("number of moves:", len(pathtogoal))
            print("number of iterations:", iters)
            break
        else:
            newstates = genstates(best)
            for i in newstates:
                if not checkstate(i, known_states):
                    i.heuristic = gradestate(i.cond)
                    heapq.heappush(states, i)
                    # states.append(i)
                    addstate(i, known_states)
    t1 = time.time()
    print("time taken:", t1 - t0)
