# This .py file contains a function to solve Sudoku using Best-First search
# Best first search algorithms is an optimized version of Backtracking,
# where the "next cell" is the cell which has the least number of possibilities
# The 'number of possibilities' is calculated for each cell, by going through its corresponding
# row, column and 3x3 block and counting the number of have-not-chosen numbers
# This greedy heuristic increase the efficiency of the program substantially, as it minimizes the branching factor.

import heapq  # Import heapq for min-heap operations

# Keep data about the "Best" cell
class EntryData:
    def __init__(self, r, c, n):
        self.row = r
        self.col = c
        self.choices = n

    def set_data(self, r, c, n):
        self.row = r
        self.col = c
        self.choices = n
    
    # Add methods for heap comparison
    def __lt__(self, other):
        return self.choices < other.choices
    
    def __eq__(self, other):
        return self.choices == other.choices

# Solve Sudoku using Best-first search
def solve_sudoku(matrix):
    cont = [True]
    # See if it is even possible to have a solution
    for i in range(9):
        for j in range(9):
            if not can_be_correct(matrix, i, j): # If it is not possible, stop
                return
    
    # Initialize the heap with all empty cells
    cell_heap = []
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:  # If it is unfilled
                num_choices = count_choices(matrix, i, j)
                heapq.heappush(cell_heap, EntryData(i, j, num_choices))
    
    sudoku_helper(matrix, cont, cell_heap)  # Pass the heap to the helper function

# Helper function - The heart of Best First Search
def sudoku_helper(matrix, cont, cell_heap):
    if not cont[0]:  # Stopping point 1
        return
    
    # If heap is empty, we've filled the board
    if not cell_heap:
        cont[0] = False  # Set the flag so that the rest of the recursive calls can stop
        return
    
    # Get the cell with the least possibilities
    best_candidate = heapq.heappop(cell_heap)
    
    row = best_candidate.row
    col = best_candidate.col
    
    # If found the best candidate, try to fill 1-9
    for j in range(1, 10):
        if not cont[0]:  # Stopping point 2
            return
        
        matrix[row][col] = j
        
        if can_be_correct(matrix, row, col):
            # Create a new heap for the next recursion
            # Note: We need to recalculate choices as they may have changed
            new_heap = []
            for i in range(9):
                for k in range(9):
                    if matrix[i][k] == 0:  # If it is unfilled
                        num_choices = count_choices(matrix, i, k)
                        heapq.heappush(new_heap, EntryData(i, k, num_choices))
            
            sudoku_helper(matrix, cont, new_heap)
    
    if not cont[0]:  # Stopping point 3
        return
    
    matrix[row][col] = 0  # Backtrack, mark the current cell empty again
    # No need to push back to heap as we're backtracking

# Count the number of choices haven't been used
def count_choices(matrix, i, j):
    can_pick = [True,True,True,True,True,True,True,True,True,True]; # From 0 to 9 - drop 0
    
    # Check row
    for k in range(9):
        can_pick[matrix[i][k]] = False

    # Check col
    for k in range(9):
        can_pick[matrix[k][j]] = False;

    # Check 3x3 square
    r = i // 3
    c = j // 3
    for row in range(r*3, r*3+3):
        for col in range(c*3, c*3+3):
            can_pick[matrix[row][col]] = False

    # Count
    count = 0
    for k in range(1, 10):  # 1 to 9
        if can_pick[k]:
            count += 1

    return count

# Return true if the current cell doesn't create any violation
def can_be_correct(matrix, row, col):
    
    # Check row
    for c in range(9):
        if matrix[row][col] != 0 and col != c and matrix[row][col] == matrix[row][c]:
            return False

    # Check column
    for r in range(9):
        if matrix[row][col] != 0 and row != r and matrix[row][col] == matrix[r][col]:
            return False

    # Check 3x3 square
    r = row // 3
    c = col // 3
    for i in range(r*3, r*3+3):
        for j in range(c*3, c*3+3):
            if row != i and col != j and matrix[i][j] != 0 and matrix[i][j] == matrix[row][col]:
                return False
    
    return True

# Return true if the whole board has been occupied by some non-zero number
# If this happens, the current board is the solution to the original Sudoku
def all_board_non_zero(matrix):
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:
                return False
    return True