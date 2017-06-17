from utils import *



"""Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

Args:
     grid: Sudoku grid in string form, 81 characters long
Returns:
     Sudoku grid in dictionary form:
     - keys: Box labels, e.g. 'A1'
     - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
"""
def grid_values(grid):
     i = 0
     puzzle = dict()
     for box in boxes:
          if grid[i] == '.':
               puzzle[box] = '123456789'
          else:
               puzzle[box] = grid[i]
          i += 1
          
     return puzzle
     pass



"""Eliminate values from peers of each box with a single value.

Go through all the boxes, and whenever there is a box with a single value,
eliminate this value from the set of values of all its peers.

Args:
     values: Sudoku in dictionary form.
Returns:
     Resulting Sudoku in dictionary form after eliminating values.
"""
def eliminate(puzzle):
     for box in puzzle:
          if len(puzzle[box]) == 1:
               digit_to_eliminate = puzzle[box]
               peers_to_check = peers[box]
               # print ('found a box with 1 value', digit_to_eliminate)
               # # print ('peers to check are', peers_to_check)
               for peer in peers_to_check:
                    if digit_to_eliminate in puzzle[peer]:
                         puzzle[peer] = puzzle[peer].replace(digit_to_eliminate, '')
          x = 0
     return puzzle
     # print ('unit list', unitlist)
     # print ('units', units['A1'])
     pass



"""Finalize all values that are the only choice for a unit.

Go through all the units, and whenever there is a unit with a value
that only fits in one box, assign the value to this box.

Input: Sudoku in dictionary form.
Output: Resulting Sudoku in dictionary form after filling in only choices.
"""
# TODO: Implement only choice strategy here

def only_choice(puzzle):

     for unit in unitlist:
          for digit in '123456789':
               # recreates a grid of a unit (all peers) filled only with 
               # boxes that contain current digit
               boxes_that_have_digit = [box for box in unit if digit in puzzle[box]]
               # print (boxes_that_have_digit)
               # if there is only 1 box in the unit that can have the current digit,
               # that digit must be a solution.
               if len(boxes_that_have_digit) == 1:
                    puzzle[boxes_that_have_digit[0]] = digit

     return puzzle
     # for box in puzzle:
     #      if len(puzzle[box]) != 1:
               
     #           for digit in puzzle[box]:
     #                # print (digit)
     #                found = False
     #                for peer in peers[box]:
     #                     if digit in puzzle[peer]:
     #                          found = True
     #                          break
     #                     # print ('not a possible solution')
     #                if found == False:
     #                     # print ('hurrah! possible solution:', digit)
     #                     puzzle[box] = digit
     # display(puzzle)
     # return puzzle


# Implements eliminate and only choice strategy until they can't be used anymore (each call makes no more changes)
# Solves simpler Sedoku puzzles
def reduce_puzzle(puzzle):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in puzzle.keys() if len(puzzle[box]) == 1])

        # Use the Eliminate Strategy
        puzzle = eliminate(puzzle)

        # Use the Only Choice Strategy
        puzzle = only_choice(puzzle)


        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in puzzle.keys() if len(puzzle[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in puzzle.keys() if len(puzzle[box]) == 0]):
            return False
    return puzzle


from utils import *

def search(puzzle):
     # "Using depth-first search and propagation, create a search tree and solve the sudoku."
     # First, reduce the puzzle using the previous function
     puzzle = reduce_puzzle(puzzle)
     if puzzle is False:
          return False ## Failed earlier
     if all(len(puzzle[s]) == 1 for s in boxes): 
          return puzzle ## Solved!
     # display(values)
     # Choose one of the unfilled squares with the fewest possibilities
     least_possibilities = 9
     least_box = None
     for box in puzzle:
          if len(puzzle[box]) < least_possibilities and len(puzzle[box]) != 1:
               least_possibilities = len(puzzle[box])
               least_box = box
               # the min we can start is 2, so if 2 then break
               if least_possibilities == 2: break
               
     # print (least_possibilities, least_box)
     # Now use recursion to solve each one of the resulting sudokus, 
     # and if one returns a value (not False), return that answer!
     for digit in puzzle[least_box]:
          new_sedoku = puzzle.copy()
          new_sedoku[least_box] = digit
          attempt = search(new_sedoku)
          if attempt:
               return attempt
        
    # If you're stuck, see the solution.py tab!


def run():
     print ('Please enter each line of the sudoku puzzle you want solved.')
     print ('For spots where the digit is notavailable, please enter \'.\',')
     print ('without the quotation marks.\n')
     print ('If you want the default puzzle solved, just hit enter at the prompt.')

     puzzle = ''
     for i in range (1, 10):
          line = input()
          if line == '': #blank enterred, jump to prebuilt puzzle
               break
          # print (line)
          puzzle += str(line)

     if puzzle != '':
          grid = grid_values(puzzle)
          print ('\nPuzzle enterred is:')
          display(grid)
          print ('\nPuzzle solution is:')
          ans = reduce_puzzle(grid)
          display(ans)
     else: #user wants pre built puzzles
          start = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
          grid = grid_values(start)
          display(grid)

          ans = reduce_puzzle(grid)
          display(ans)

          print ('\nNow the harder puzzle will be solved')
          harderPuzzle = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
          grid2 = grid_values(harderPuzzle)
          ans2 = search(grid2)

          display(ans)
run()