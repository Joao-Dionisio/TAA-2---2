Advanced Topics in Algorithms - Module 2
Assignment 2 [1]
Professor: João Pedro Pedroso 

Implementation of several heuristics to solve the resource contrainted project scheduling problem (RCPSP). They are the Serial Scheduling Scheme [2], and two ways of transversing the solution tree, BFS-cut_short - a variant of BFS, and Beam Search. 



Built with: Python 3.7 (Important! Will not work on Python 3.6 or lower, due to the use of a recently updated library - queue)



###########
Instructions
###########

Simply run the program you're interested in, paying attention to what's at the bottom of the file, the test cases. There are two blocks of test cases, one refering to the J30 dataset and the other refering to the J60 dataset [3]. As was agreed in our class, we tested our code only for first instance of every sub-block, which is to say, we only tested the code for one dataset every 10 datasets. By default, the J30 test is uncommented and the J60 test is commented. 

To run SGS, simply type:

> Python sgs.py [path/to/file]

If path is ommited, then it runs the benchmark proposed in the Slack Server.

For the BFS, before running, you should note the integer parameter in start_complete_search. It refers to the number of levels the bfs will explore before forcing a solution. Be advised that for bigger values (>5) it starts to take a really long time. We initialized it to 0.

For the beam search, you need to pay attention to the same thing. The function start_beam_search has an integer parameter, related to the maximum number of partial solutions that will be investigated. For the J30 it takes quite a bit less that te BFS, but it still takes a while for bigger values (>10). Also, be aware that, for values > 5, the solutions actually start worsening, as we discussed in the report.




Authors:

	João Dionísio   - FCUP
	Rodrigo Marques - FCUP
			

References:

[1] - https://www.dcc.fc.up.pt/~jpp/taa/assignment-02.pdf
[2] - https://pdfs.semanticscholar.org/73fc/d16cf279ee407da01a7471d4f6b61f610bae.pdf?_ga=2.130559503.1484643935.1589746790-1360775320.1589659443
[3] - http://www.om-db.wi.tum.de/psplib/getdata_sm.html
