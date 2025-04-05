import numpy as np

def calculate_difficulty(grid):
    """
    Analyzes a Sudoku grid to determine its difficulty level.
    Returns a tuple: (difficulty_level, score)
    
    Difficulty is based on several factors:
    1. Number of empty cells (more cells = harder)
    2. Pattern of given cells (symmetry is usually easier)
    3. Required solving techniques
    
    Difficulty levels:
    - Easy: Score < 40
    - Medium: Score 40-60
    - Hard: Score 60-80
    - Expert: Score > 80
    """
    grid_array = np.array(grid)
    
    # Count empty cells (0s) - optimized with numpy
    empty_cells = np.count_nonzero(grid_array == 0)
    
    # Symmetry check
    symmetry_score = check_symmetry(grid)
    
    # Calculate "isolation factor" - how spread out are the given numbers
    isolation_factor = calculate_isolation(grid)
    
    # Calculate "regional density" - are there regions with very few clues?
    regional_density = calculate_regional_density(grid)
    
    # Calculate solving technique score
    technique_score = estimate_solving_techniques(grid)
    
    # Calculate final score (0-100 scale)
    # Weight the factors accordingly
    final_score = (
        min(empty_cells * 1.5, 45) +  # Max 45 points from empty cells
        technique_score * 0.35 +      # Max 35 points from techniques
        (10 - symmetry_score) * 0.1 + # Max 10 points from asymmetry
        isolation_factor * 0.05 +     # Max 5 points from isolation
        regional_density * 0.05       # Max 5 points from regional sparsity
    )
    
    # Determine difficulty level based on final score
    if final_score < 40:
        return "Easy", final_score
    elif final_score < 60:
        return "Medium", final_score
    elif final_score < 80:
        return "Hard", final_score
    else:
        return "Expert", final_score

def check_symmetry(grid):
    """
    Checks how symmetrical the puzzle is.
    Returns a score from 0-10, where 10 is perfectly symmetrical.
    """
    symmetry_count = 0
    total_checks = 0
    
    for i in range(9):
        for j in range(9):
            # Check rotational symmetry (180 degrees)
            opposite_i = 8 - i
            opposite_j = 8 - j
            
            # Don't double count the center cell
            if i == opposite_i and j == opposite_j:
                continue
                
            total_checks += 1
            # Both cells should either be filled or empty for symmetry
            if (grid[i][j] == 0) == (grid[opposite_i][opposite_j] == 0):
                symmetry_count += 1
    
    # Return score out of 10
    return round(10 * symmetry_count / total_checks) if total_checks > 0 else 10

def calculate_isolation(grid):
    """
    Calculates how isolated the given numbers are.
    Returns a score from 0-10, where 10 means highly isolated numbers.
    """
    isolation_score = 0
    filled_cells = []
    
    # Find all filled cells
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                filled_cells.append((i, j))
    
    if not filled_cells:
        return 0
    
    # Calculate average distance between filled cells
    total_distance = 0
    comparisons = 0
    
    for i, cell1 in enumerate(filled_cells):
        for cell2 in filled_cells[i+1:]:
            manhattan_distance = abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])
            total_distance += manhattan_distance
            comparisons += 1
    
    if comparisons == 0:
        return 0
        
    avg_distance = total_distance / comparisons
    # Normalize to 0-10 scale (maximum Manhattan distance is 16)
    return min(10, avg_distance * 10 / 8)

def calculate_regional_density(grid):
    """
    Calculates how sparse some regions are compared to others.
    Returns a score from 0-10, where 10 means high variation in regional density.
    """
    # Count filled cells in each 3x3 box
    box_counts = [0] * 9
    
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                box_index = (i // 3) * 3 + (j // 3)
                box_counts[box_index] += 1
    
    # Calculate variance in box counts
    avg_count = sum(box_counts) / 9
    variance = sum((count - avg_count) ** 2 for count in box_counts) / 9
    
    # Normalize to 0-10 scale (maximum variance would be around 9)
    return min(10, variance * 10 / 5)

def estimate_solving_techniques(grid):
    """
    Estimates the solving techniques required based on grid analysis.
    Returns a score from 0-100, where higher means more advanced techniques.
    """
    # This is a simplified estimation - a full implementation would 
    # actually try different solving techniques
    
    # Count naked singles (cells with only one possible value)
    naked_singles = count_naked_singles(grid)
    
    # Fewer naked singles means harder puzzle
    if naked_singles > 15:
        return 10  # Very easy - mostly naked singles
    elif naked_singles > 10:
        return 30  # Easy - many naked singles
    elif naked_singles > 5:
        return 60  # Medium - some naked singles
    else:
        return 90  # Hard/Expert - very few naked singles

def count_naked_singles(grid):
    """
    Counts how many cells have only one possible value.
    """
    count = 0
    
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:  # Empty cell
                possibilities = get_possibilities(grid, i, j)
                if len(possibilities) == 1:
                    count += 1
                    
    return count

def get_possibilities(grid, row, col):
    """
    Returns the possible values for a cell at (row, col).
    """
    if grid[row][col] != 0:
        return []
        
    possibilities = set(range(1, 10))
    
    # Check row
    for c in range(9):
        if grid[row][c] != 0:
            possibilities.discard(grid[row][c])
    
    # Check column
    for r in range(9):
        if grid[r][col] != 0:
            possibilities.discard(grid[r][col])
    
    # Check 3x3 box
    box_row, box_col = (row // 3) * 3, (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if grid[r][c] != 0:
                possibilities.discard(grid[r][c])
    
    return possibilities

def is_valid_sudoku(grid):
    """
    Checks if a Sudoku grid is valid (no duplicates in rows, columns, or boxes).
    Returns (True, None) if valid or (False, error_message) if invalid.
    """
    # Check rows
    for row in range(9):
        values = {}
        for col in range(9):
            val = grid[row][col]
            if val != 0:
                if val in values:
                    return False, f"Duplicate {val} in row {row+1}"
                values[val] = True
    
    # Check columns
    for col in range(9):
        values = {}
        for row in range(9):
            val = grid[row][col]
            if val != 0:
                if val in values:
                    return False, f"Duplicate {val} in column {col+1}"
                values[val] = True
    
    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            values = {}
            for row in range(box_row, box_row + 3):
                for col in range(box_col, box_col + 3):
                    val = grid[row][col]
                    if val != 0:
                        if val in values:
                            return False, f"Duplicate {val} in 3x3 box at position ({box_row//3+1},{box_col//3+1})"
                        values[val] = True
    
    # Check if the puzzle has a solution
    test_grid = [row[:] for row in grid]  # Make a deep copy
    solution_exists = check_solution_exists(test_grid)
    if not solution_exists:
        return False, "Puzzle has no solution"
    
    return True, None

def check_solution_exists(grid):
    """
    Quick check if a solution might exist by testing a few steps.
    Note: This is not a complete solver but a quicker validity check.
    """
    # Check if any cell has no valid options
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                possibilities = get_possibilities(grid, i, j)
                if not possibilities:
                    return False  # No options for this cell means no solution
    
    return True  # Passed the quick check - solution might exist