import sys
import queue
from copy import copy, deepcopy

from data import *
from sgs import *

def entry(prob, cmax, max_depth):
    sol = Solution(prob)
    sol.backward_pass()
    sol.schedule(id=0, start_time=0)
    best = [cmax]
    return sgs_search(sol, 1, [cmax], max_depth)


def sgs_search(sol, index, best, max_depth):
    if index < max_depth:
        sol.calc_eligible()

        finish_times = [sol.finish_time[j] for j in sol.scheduled]

        remaining = {}
        for t in finish_times:
            remaining[t] = sol.calc_remaining(t)
    
        for j in sol.eligible:
            new_sol = deepcopy(sol)
            new_sol.eligible.remove(j)
            job = new_sol.prob.jobs[j]

            EF = max([new_sol.finish_time[h] for h in job.predecessors]) + job.duration
            LF = new_sol.latest_finish[j]

            possible_times = [t for t in finish_times if t <= LF - job.duration and t >= EF - job.duration]
            feasible_times = []
            for t in possible_times:
                taus = [tau for tau in finish_times if tau < t + job.duration and tau >= t]
                if all([is_resource_feasible(job, remaining[tau]) for tau in taus]):
                    feasible_times.append(t)

            start = min(feasible_times)
            new_sol.schedule(start, j)  
            times = sgs_search(new_sol, index + 1, best, max_depth)

            if times[-1] < best[-1]:
                best = times

        return best

    else: return sgs_(sol)

def sgs_(sol):

    for i in range(len(sol.unprocessed)):
        sol.calc_eligible()

        finish_times = [sol.finish_time[j] for j in sol.scheduled]

        remaining = {}
        for t in finish_times:
            remaining[t] = sol.calc_remaining(t)

        j = sol.select()
        job = sol.prob.jobs[j]

        EF = max([sol.finish_time[h] for h in job.predecessors]) + job.duration
        LF = sol.latest_finish[j]

        possible_times = [t for t in finish_times if t <= LF - job.duration and t >= EF - job.duration]
        feasible_times = []
        for t in possible_times:
            taus = [tau for tau in range(t, t + job.duration) if tau in finish_times]
            if all([is_resource_feasible(job, remaining[tau]) for tau in taus]):
                feasible_times.append(t)

        start = min(feasible_times)
        sol.schedule(start, j)

    sol.finish_time[-1] = max(sol.finish_time)
    return sol.finish_time


def benchmark(max_depth):
    start = time.time()
    prefix30 = "data/j30/j30"
    prefix60 = "data/j60/j60"
    suffix = "_1.sm"

    end_times = []
    
    for i in range(1, 49):
        filename = f"{prefix30}{i}{suffix}"
        prob  = read_file(filename)
        
        sol = sgs(prob)
        times = entry(prob, sol.finish_time[-1], max_depth)
        print(times)
        end_times.append(times[-1])

    print(f"j30: {end_times}")
    print(sum(end_times))
    print(f"test completed in {(time.time()-start)} seconds!")

    start = time.time()
    end_times = []
    
    for i in range(1, 49):
        filename = f"{prefix60}{i}{suffix}"
        prob  = read_file(filename)
        
        sol = sgs(prob)
        times = entry(prob, sol.finish_time[-1], max_depth)
        print(times)
        end_times.append(times[-1])
    
    print(f"j60: {end_times}")
    print(f"test completed in {(time.time()-start)} seconds!")

import time

if __name__ == "__main__":
    if len(sys.argv) == 1:
        benchmark(5)
    
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        prob = read_file(filename)
        initial = sgs(prob)
        print(initial.finish_time[-1])
        sol  = entry(prob, initial.finish_time[-1], 5)
        print(sol)

    elif len(sys.argv) == 3:
        filename = sys.argv[1]
        if filename == "benchmark":
            benchmark(int(sys.argv[2]))
        else:
            prob = read_file(filename)
            initial = sgs(prob)
            print(initial.finish_time[-1])
            sol  = entry(prob, initial.finish_time[-1], int(sys.argv[2]))
        print(sol)
    else:
        print(
"""
Usage: python dfs2.py [filename] [max-depth]
Default filename: benchmark
Default depth: 5
""")
        
