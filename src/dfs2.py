from copy import copy
from sgs import *
import time

def start_complete_search(prob, n_levels):
    global completeSearch
    completeSearch = []
    sol = Solution(prob)
    sol.backward_pass()
    sol.schedule(id=0, start_time=0)

    complete_search(sol, 0, n_levels)
    possible_solutions = []

    for i in completeSearch:
        possible_solutions.append(sgs_partial(i))

    min = float('inf')
    for i in possible_solutions:
        if max(i.finish_time) < min:
            min = max(i.finish_time)

    return min


def complete_search(parent_solution, recursion_level, n_levels):
    '''
    Runs a complete search on the solution tree to the RCPSP problem. Performs a BFS on all possible solutions until a certain level
    (n_levels). The levels represent the number of activities scheduled, so if n_levels = 5, we will find all possible ways of scheduling
    5 activities, starting from activity 0. When we reach n_levels, we go down the solution tree until we find a complete solution to our 
    problem, using the sgs algorithm.

    Parameters:

    parent_solution: The partial solution from whom we'll pursue all possible paths, at a given level.
    recursion_level: The number of scheduled activities of the parent solution.
    n_levels:        The number of levels we want to to fully explore.
    '''
    global completeSearch
    parent_solution.calc_eligible()
    if recursion_level < n_levels:
        finish_times = [parent_solution.finish_time[j] for j in parent_solution.scheduled]
        
        remaining = {}
        for t in finish_times:
            remaining[t] = parent_solution.calc_remaining(t)

        for j in parent_solution.eligible:
            temp_sol = deepcopy(parent_solution)
            temp_sol.eligible.remove(j)
            job = temp_sol.prob.jobs[j]

            EF = max([temp_sol.finish_time[h] for h in job.predecessors]) + job.duration
            LF = temp_sol.latest_finish[j]

            possible_times = [t for t in range(EF - job.duration, LF-job.duration) if t in finish_times]
            feasible_times = []
            for t in possible_times:
                taus = [tau for tau in range(t, t+job.duration) if tau in finish_times]
                if all([is_resource_feasible(job, remaining[tau]) for tau in taus]):
                    feasible_times.append(t)

            start = min(feasible_times)
            temp_sol.schedule(start, j)
            complete_search(temp_sol, recursion_level+1, n_levels)

    # If we reached the number of explored paths, we store the partial solution for later and we stop the search
    if recursion_level == n_levels:
        completeSearch.append(parent_solution)
        return


def benchmark(max_depth):
    start30 = time.time()
    results30 = []

    global completeSearch
    global upper_bound
    for i in range(1, 49):
        completeSearch = []
        file = "data/j30/j30" + str(i) + "_1.sm"
        prob = read_file(file)
        upper_bound = max(sgs(prob).finish_time)
        sol  = start_complete_search(prob, max_depth)
        print("j30" + str(i) + "_1.sm done!")
        results30.append(sol)
    finish30 = time.time()
    results60 = []
    start60 = time.time()
    for i in range(1, 49):
        completeSearch = []
        file = "data/j60/j60" + str(i) + "_1.sm"
        prob = read_file(file)
        sol  = start_complete_search(prob, max_depth)
        print("j60" + str(i) + "_1.sm done!")
        results60.append(sol)
    finish60 = time.time()

    print(f"J30 test completed in {(finish30 - start30)} seconds!")
    print(results30)
    print("The sum was ", sum(results30))
    print()
    print(f"J60 test completed in {(finish60 - start60)} seconds!")
    print(results60)
    print("The sum was ", sum(results60))

def run(filename, depth):
    prob    = read_file(filename)
    sol     = start_complete_search(prob, depth)
    print(sol)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        benchmark(4)

    elif len(sys.argv) == 2:
        run(sys.argv[1], 4)
        
    elif len(sys.argv) == 3:
        if sys.argv[1] == "benchmark":
            benchmark(int(sys.argv[2]))
        else:
            run(sys.argv[1], int(sys.argv[2]))
    else:
        print(
"""
Usage: python dfs.py [filename] [max-depth]
Default filename: benchmark
Default depth: 5
""")
