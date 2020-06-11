from copy import copy
from sgs import *
import time

def start_complete_search(prob, n_levels):
    sol = Solution(prob)
    sol.backward_pass()
    sol.schedule(id=0, start_time=0)
    complete_search(sol, 0, n_levels)
    possible_solutions = []

    for i in completeSearch:
        possible_solutions.append(get_solution(i))

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
    
    
def get_solution(sol):
    '''
    Runs the sgs algorithm, but on a project that already started being planned
    '''
    for i in range(1, len(sol.unprocessed)):
        sol.calc_eligible()

        finish_times = [sol.finish_time[j] for j in sol.scheduled]

        remaining = {}
        for t in finish_times:
            remaining[t] = sol.calc_remaining(t)
        
        j = sol.select()
        job = sol.prob.jobs[j]

        EF = max([sol.finish_time[h] for h in job.predecessors]) + job.duration
        LF = sol.latest_finish[j]

        possible_times = [t for t in range(EF - job.duration, LF - job.duration) if t in finish_times]
        feasible_times = []
        for t in possible_times:
            taus = [tau for tau in range(t, t + job.duration) if tau in finish_times]
            if all([is_resource_feasible(job, remaining[tau])for tau in taus]):
                feasible_times.append(t)
        start = min(feasible_times)
        sol.schedule(start, j)
        
    sol.finish_time[-1] = max(sol.finish_time)
    return sol


if __name__ == "__main__":
    start = time.time()
    results = []

    global completeSearch
    for i in range(1, 49):
        completeSearch = []
        file = "data/j30/j30" + str(i) + "_1.sm"
        prob = read_file(file)
        sol  = start_complete_search(prob,5)
        print("j30" + str(i) + "_1.sm done!")
        results.append(sol)

    for i in range(1, 49):
        completeSearch = []
        file = "data/j60/j60" + str(i) + "_1.sm"
        prob = read_file(file)
        sol  = start_complete_search(prob,1)
        print("j30" + str(i) + "_1.sm done!")
        results.append(sol)

    print(results)
    print(f"test completed in {(time.time()-start)} seconds!")


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        prob = read_file(filename)
        sol  = start_complete_search(prob)
        print(sol.finish_time)
    except IndexError:
        benchmark()
    
