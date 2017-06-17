# A simple Python3 based sudoku ai
AI uses constraint propagation to reduce problem size down to a solvable puzzle. For easy puzzles, this should be enough to solve the problem
In the case that the problem is a more difficult puzzle, ai uses elimination and only one strategies to reduce problem size. Then AI recursivly calls itself, filling in random values in puzzle boxes not yet solved, until one call produces a solution

# Constraint Propagation Strategies
## Strategy 1: Elimination
If a box has a solved value, than none of its peers can have the same value. Peers are other boxes in the same row, column, or 3x3 grid. Elimination function goes through all these peers and removes discovered value from list of possible solutions.

## Strategy 2: Only Choice
If there is only 1 box in a unit which would allow a certain value, than that box must be assined that digit. A unit is a boxes possible peers, ie boxes in same row, column, and 3x3 grid. Visually, this looks like:
 insert visual here

In example above, the only box that has 1 as a possible solution is the top right box. only_choice() discovers that, and puts 1 in top right box

## Strategy 3: Recursive Search (When strats 1 & 2 looped fail to solve problem):
Called when a puzzle is more challenging and requires more work than repeated calls to strategies 1 and 2. Picks a box with a minimal number of possible values (box is either 1 or a 2). Trys to solve puzzle by creating new puzzle with pozzible values inserted, and recursivly calls main puzzle solving function (loop of strategy 1 and 2).