# Blocksworld

This program solves the blocksworld problem using A* search.

## Command Line Arguments

There is one **required** command line argument, the name of a file containing the problem definition (i.e. probA03.bwp). 
The program will attempt to open the file with that name *in a folder titled "probs"* in the same directory as the program. 
If the file is not found, the program will error out.

There are two **optional** command line arguments, which are **-H** to specify the heuristic function to use and **-MAX_ITER** to specify the maximum number of iterations to run the search algorithm for.

The **-H** argument can be followed by one of the following options:
- **H0**: This runs breadth-first search, which is equivalent to A* search with the heuristic function h(n) = 0.
- **H1**: This runs A* search with my best heuristic, which is also the program's default (described below).
- **H2**: This runs A* search with a simple heuristic that counts the number of blocks that are in the wrong stack and adds that to the path length.

The **-MAX_ITER** argument can be followed by any positive integer. If it is not specified, the program will assume a default value of 1,000,000.

## Constraints

The program assumes that the problem definition file is formatted correctly. There are no known limits on what the best heuristic can calculate in terms of number of stacks, but the problems must contain 26 blocks or less for the encoding to function properly.

## Heuristic Function

The best heuristic function (used by default) is the sum of the following three values:
- The path length
- Twice the number of blocks that are in the wrong stack
- The number of blocks that are at the wrong height in their stack, plus twice the difference between their current and their correct height
This biases the function away from focusing solely on finding the shortest path by multiplying the other heuristic components by > 1. Higher biases cause certain problem types (e.g. probB13.bwp) to take much longer to solve to the benefit of others (e.g. probB19.bwp), while lower biases cause the opposite.