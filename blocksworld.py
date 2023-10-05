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
        self.pathcost = 0;

    def __lt__(self, other):
        return self.heuristic < other.heuristic

    def __eq__(self, other):
        return self.cond == other.cond

    def __str__(self):
        return str(self.cond) + " " + str(self.heuristic)

def H0(state):
    return 0
    
# grades a state and assigns heuristic value
def H1(state):
    h = state.pathcost
    for i in range(0, len(state.cond)):
        for j in range(0, len(state.cond[i])):
            if i != goalMap[state.cond[i][j]][0]:
                h += 2
            if j != goalMap[state.cond[i][j]][1]:
                h += 1 + (2 * abs(j - goalMap[state.cond[i][j]][1]))
    return h


# grades a state and assigns heuristic value
def H2(state):
    h = state.pathcost
    for i in range(0, len(state.cond)):
        for j in range(0, len(state.cond[i])):
            if i != goalMap[state.cond[i][j]][0]:
                h += 1 + len(state.cond[i]) - j
    return h

MAX_ITERS = 1000000
gradestate = H1
BFS = False
heuristicName = "Best heuristic (A*, H1)"
for i in range(0, len(args)):
    if len(args) > i and args[i] == "-H":
        if args[i + 1] == "H0":
            gradestate = H0
            heuristicName = "BFS (H0)"
            BFS = True
        elif args[i + 1] == "H1":
            gradestate = H1
            heuristicName = "Best Heuristic (A*, H1)"
        elif args[i + 1] == "H2":
            gradestate = H2
            heuristicName = "Simple Heuristic (A*, H2)"
        else:
            print("Invalid heuristic")
            exit()
    if len(args) > i and args[i] == "-MAX_ITERS":
        if args[i + 1].isnumeric():
            MAX_ITERS = int(args[i + 1])
        else:
            print("Invalid max iterations")
            exit()


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
            newstate.pathcost = parent_state.pathcost + 1
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
    print("\033[33mStarting State:\033[0m", cond)
    print("\033[33mGoal:\033[0m", goal)
    print("\033[33mUsing heuristic:\033[0m", heuristicName)
    ancestor_state = state(cond, 0)
    ancestor_state.heuristic = gradestate(ancestor_state)
    states = genstates(ancestor_state)
    iters = 0
    for i in states:
        i.heuristic = gradestate(i)
    known_states = dict()
    addstate(ancestor_state, known_states)
    if not BFS:
        heapq.heapify(states)
    max_heap_size = 0
    while len(states) > 0:
        if len(states) > max_heap_size:
            max_heap_size = len(states)
        if iters >= MAX_ITERS:
            print(f"\n\033[31mMax Iters ({MAX_ITERS}) Reached!")
            print("Current State:\033[0m", best.cond)
            print()
            break
        iters += 1
        if not BFS:
            best = heapq.heappop(states)
        else:
            best = states.pop(0)
        if best.cond == goal:
            print("\033[32m\nGoal reached!")
            pathtogoal = []
            while best.parent is not None:
                pathtogoal.append(best)
                best = best.parent
            print("Path to Goal:\033[0m")
            print(ancestor_state.cond, "\033[33m<- Start\033[0m")
            for i in pathtogoal[::-1]:
                if i == pathtogoal[0]:
                    print(goal, "\033[33m<- Goal\033[0m")
                else:
                    print(i.cond)
            pathLength = len(pathtogoal)
            print(f"\n\033[33mStatistics: \033[34m{filename}\033[0m, Method: \033[34m{heuristicName}\033[0m, Moves: \033[34m{pathLength}\033[0m, Iterations: \033[34m{iters}\033[0m, Max Heap Size: \033[34m{max_heap_size}\033[0m")
            break
        else:
            newstates = genstates(best)
            for i in newstates:
                if not checkstate(i, known_states):
                    i.heuristic = gradestate(i)
                    if not BFS:
                        heapq.heappush(states, i)
                    else:
                        states.append(i)
                    addstate(i, known_states)
    t1 = time.time()
    print("\033[33mTime Taken:\033[0m", t1 - t0)
    print()
