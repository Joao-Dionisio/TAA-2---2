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

Simply run the program you're interested in, paying attention to what's at the bottom of the file, the test cases. There are two blocks of test cases, one refering to the J30 dataset and the other refering to the J60 dataset [3]. As was agreed in our class, we tested our code only for first instance of every sub-block, which is to say, we only tested the code for one dataset every 10 datasets. By default, the J30 test is uncommented and the J60 test is commented.

## Complete search

For the BFS, before running, you should note the integer parameter in start_complete_search. It refers to the number of levels the bfs will explore before forcing a solution. Be advised that for bigger values (>5) it starts to take a really long time. We initialized it to 0.

For the beam search, you need to pay attention to the same thing. The function start_beam_search has an integer parameter, related to the maximum number of partial solutions that will be investigated. For the J30 it takes quite a bit less that te BFS, but it still takes a while for bigger values (>10). Also, be aware that, for values > 5, the solutions actually start worsening, as we discussed in the report.

## References

  1) <https://www.dcc.fc.up.pt/~jpp/taa/assignment-02.pdf>

  2) <https://pdfs.semanticscholar.org/73fc/d16cf279ee407da01a7471d4f6b61f610bae.pdf?_ga=2.130559503.1484643935.1589746790-1360775320.1589659443>

  3) <http://www.om-db.wi.tum.de/psplib/getdata_sm.html>
