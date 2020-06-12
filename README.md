# Advanced Topics in Algorithms - Assignment 2 [1]

Professor: João Pedro Pedroso

Authors: João Dionísio, Rodrigo Marques

Implementation of several heuristics to solve the resource contrainted project scheduling problem (RCPSP). They are the Serial Scheduling Scheme [2], and two ways of transversing the solution tree, BFS-cut_short - a variant of BFS, and Beam Search.

## Requirements

- Python 3.7 (queue)

## Running

### - SGS

Pass the file you want to solve for as an argument. The output will be the list of final times for each activity. The total span of the project is the final time of the last activity.

Example: `> python sgs.py data/j30/j301_1.sm`

Output: `[0, 8, 12, 6, 15, 16, 17, 21, 8, 13, 17, 23, 18, 26, 24, 26, 32, 23, 24, 33, 34, 39, 41, 44, 36, 24, 42, 47, 40, 49, 49, 49]`

To run the proposed benchmark (first instance of each parameter set) just run the program with no arguments. In this case the output will be a list of all project spans, grouped by dataset.

Output:

`j30: [49, 44, 88, 49, 68, 64, 55, 44, 100, 56, 65, 47, 75, 56, 46, 51, 66, 55, 41, 57, 97, 46, 63, 53, 120, 72, 47, 69, 95, 54, 43, 61, 66, 69, 65, 66, 88, 50, 59, 51, 104, 63, 62, 50, 97, 69, 65]`

`j60: [80, 70, 62, 84, 98, 70, 78, 64, 108, 91, 71, 59, 134, 69, 84, 64, 101, 97, 63, 60, 118, 73, 83, 65, 148, 94, 96, 92, 141, 84, 65, 69, 114, 78, 90, 61, 120, 89, 81, 86, 169, 87, 122, 84, 121, 91, 75]`

## Complete search

Files: dfs.py, dfs2.py, beam-search.py

All files take arguments as in:

`> python prog.py [filename] [int-parameter]`

To run the benchmark:

`> python prog.py`

To run the benchmark with a diferent bound:

`> python prog.py benchmark [bound]`

To run for a specific file (bound can be ommited):

`> python prog.py [path/to/file] [bound]`

The first dfs is slower and consumes gigabytes of memory but produces better results. The second dfs is much faster and wastes little memory but produces worse results. Maximum depth can be passed as an argument when running the program. For dfs.py set the depth to 6 or lower, for dfs2.py set it to 7 or lower.

For the beam-search, the beam width can be passed as a paremeter. Set it to 2 or lower.

## References

  1) <https://www.dcc.fc.up.pt/~jpp/taa/assignment-02.pdf>

  2) <https://pdfs.semanticscholar.org/73fc/d16cf279ee407da01a7471d4f6b61f610bae.pdf?_ga=2.130559503.1484643935.1589746790-1360775320.1589659443>

  3) <http://www.om-db.wi.tum.de/psplib/getdata_sm.html>
