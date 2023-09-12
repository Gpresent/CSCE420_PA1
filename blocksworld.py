import sys

args = sys.argv[1:]
filename = args[0]

#generates all possible next states from current state
def genstates(state):
    states = []
    for i in range(0, len(state)):
        if state[i] == '':
            continue
        for j in range(1, len(state)):
            newstate=state.copy()
            lastdig = newstate[i][-1]
            newstate[i] = newstate[i][0:-1]
            newstate[(i+j)%len(state)] += lastdig
            states.append(newstate)
    return states

    
with open("probs/" + filename, 'r') as f:
    # read basic file info
    lines = f.readlines()
    col_num, block_num, move_num = lines[0].strip().split()
    col_num = int(col_num)
    block_num = int(block_num)
    move_num = int(move_num)

    # read initial state and goal state from file
    state = []
    line_num = 2
    for i in range(0, col_num):
        state.append(lines[line_num + i].strip())
    line_num += int(col_num) + 1
    goal = []
    for i in range(0, col_num):
        goal.append(lines[line_num + i].strip())
    
    # debug printouts
    print("state:", state)
    print("goal:", goal)
    states = genstates(state)


    d = dict()
    for s in states:
        d[s] = 1
    print("possible states:", states)

