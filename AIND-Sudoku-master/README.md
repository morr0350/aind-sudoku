# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: *Student should provide answer here*

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: *Student should provide answer here*

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.

Project questions:
1) How do we apply constraint propagation to solve the naked twins problem?
We apply constraint propagation to solve the naked twins problem by considering the local problem space (the current row
or column) for each box and applying the constraint (peer boxes cannot contain either of the two digits present in
 the naked twin boxes) to that local space.  We do this for the entire problem space to reduce the problem size.
2) How do we apply constraint propagation to solve the diagonal sudoku problem?
We apply constraint propagation to solve the diagonal sudoku problem by considering the local problem space of the
diagonals (positive: lower right to upper left, and negative: upper left to lower right) for any box contained in
one of those diagonals.  We add this to the overall local problem space of each box, so that if any box is in a
diagonal, its local space is increased to add the diagonal sudoku constraint.