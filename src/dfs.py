import sys
import queue
from copy import copy, deepcopy

from data import *
from sgs import *


def entry(prob, worst):
    sol = Solution(prob)
    sol.backward_pass()
    sol.schedule(id=0, start_time=0)
    return sgs_search(sol, 1, [999], worst)


def sgs_search(sol, index, best, worst):
    if index == sol.prob.njobs:
        return sol.finish_time

    if index < 3:
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

            t = min(feasible_times)

            if t + sol.prob.jobs[j].duration >= best[-1]:
                return [999]

            new_sol.schedule(t, j)  

            times = sgs_search(new_sol, index + 1, best, worst)

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

        # Add job to solution
        sol.schedule(start, j)

    return sol.finish_time


def benchmark():
    prefix30 = "data/j30/j30"
    prefix60 = "data/j60/j60"
    suffix = "_1.sm"

    end_times = []
    
    for i in range(1,49):
        filename = f"{prefix30}{i}{suffix}"
        prob  = read_file(filename)
        
        sol = sgs(prob)
        times = entry(prob, sol.finish_time[-1])
        print(times)
        end_times.append(times[-1])

    print(f"j30: {end_times}")

    # end_times = []

    # for i in range(1,48):
    #     filename = f"{prefix60}{i}{suffix}"
    #     prob = read_file(filename)
    #     sol = sgs(prob)
    #     end_times.append(sol.finish_time[-1])
    
    # print(f"j60: {end_times}")

import time

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        prob = read_file(filename)
        initial = sgs(prob)
        print(initial.finish_time[-1])
        sol  = entry(prob, initial.finish_time[-1])
        print(sol)
    except IndexError:
        start = time.time()
        benchmark()
        print(f"test completed in {(time.time()-start)} seconds!")
    