assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

"""
Set up collections to hold game board box references
"""
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diag_unit_positive = [[x+y for x in rows for y in cols if (8-rows.index(x)) == cols.index(y)]]
diag_unit_negative = [[x+y for x in rows for y in cols if rows.index(x) == cols.index(y)]]
unitlist = row_units + column_units + square_units + diag_unit_positive + diag_unit_negative
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    naked_twins_rows = []
    naked_twins_cols = []
    for row in row_units:
        for box in row:
            for other in row:
                if box != other and len(values[box]) == 2 and len(values[other]) == 2 and \
                    all([num in values[box] for num in values[other]]) and \
                    (box, other) not in naked_twins_rows and \
                        (other, box) not in naked_twins_rows:
                    naked_twins_rows.append((box, other))

    for col in column_units:
        for box in col:
            for other in col:
                if box != other and len(values[box]) == 2 and len(values[other]) == 2 and \
                    all([num in values[box] for num in values[other]]) and \
                    (box, other) not in naked_twins_cols and \
                        (other, box) not in naked_twins_cols:
                    naked_twins_cols.append((box, other))

    row_dict = dict((s, [u for u in row_units if s in u]) for s in boxes)
    for twins in naked_twins_rows:
        this_row = row_dict[twins[0]][0]
        peers = [box for box in this_row if box not in twins]
        for peer in peers:
            for twin in twins:
                if len(values[peer]) > 1:
                    for num in values[twin]:
                        values = assign_value(values, peer, values[peer].replace(num, ""))

    col_dict = dict((s, [u for u in column_units if s in u]) for s in boxes)
    for twins in naked_twins_cols:
        this_col = col_dict[twins[0]][0]
        peers = [box for box in this_col if box not in twins]
        for peer in peers:
            for twin in twins:
                if len(values[peer]) > 1:
                    for num in values[twin]:
                        values = assign_value(values, peer, values[peer].replace(num, ""))

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grid_dict = dict(zip(boxes, grid))
    return {x: y.replace('.', '123456789') for x,y in grid_dict.items()}


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    from PySudoku import play
    play(assignments)


def eliminate(values):
    """
    :param values(dict): a dictionary of the form {'box_name': '123456789', ...}
    :return: values dict or False
    Apply constraint that if a box has a value assigned, then none of the peers of this box can have this value.
    """
    for box in values.keys():
        if len(values[box]) == 1:
            for peer in peers[box]:
                # values[peer] = values[peer].replace(values[box], "")
                if len(values[peer]) > 1:
                    values = assign_value(values, peer, values[peer].replace(values[box], ""))
    values = naked_twins(values)
    return values

def only_choice(values):
    """
    :param values(dict): a dictionary of the form {'box_name': '123456789', ...}
    :return: values dict or False
    Apply constraint that every local space unit must contain exactly one occurrence of every number
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                # values[dplaces[0]] = digit
                values = assign_value(values, dplaces[0], digit)
    return values


def reduce_puzzle(values):
    """
    :param values(dict): a dictionary of the form {'box_name': '123456789', ...}
    :return: values dict or False
    Applies constraints to reduce the game board problem size (solve or partially solve
    as many sudoku squares as possible)
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        if solved_values_before == len(values.keys()):
            break
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
    :param values: game board dict
    :return: values dict or False
    Using depth-first search and propagation, create a search tree and solve the sudoku.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(value) == 1 for key, value in values.items()):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    fewest_nums, box_with_fewest = min((len(y), x) for x, y in values.items() if len(y) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for digit in values[box_with_fewest]:
        new_sudoku = values.copy()
        new_sudoku[box_with_fewest] = digit
        sudoku_branch = search(new_sudoku)
        if sudoku_branch:
            return sudoku_branch


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
