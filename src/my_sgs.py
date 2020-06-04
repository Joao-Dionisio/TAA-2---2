import sys
import queue
from copy import copy, deepcopy

from data import *

class Solution:
    def __init__(self, prob):
        self.prob = deepcopy(prob)

        self.finish_time     = [0] * prob.njobs

        self.earliest_start  = [0] * prob.njobs
        self.earliest_finish = [0] * prob.njobs
        self.latest_start    = [0] * prob.njobs
        self.latest_finish   = [0] * prob.njobs

        # set of scheduled job ids
        self.scheduled = set()

        # set of jobs that can be scheduledt
        self.eligible = set()

        # set of unprocessed jobs
        self.unprocessed = list(range(0, prob.njobs))


    def calc_eligible(self):
        eligible = set()

        for j in self.unprocessed:
            job = self.prob.jobs[j]
            if job.is_ready():
                eligible.add(j)

        self.eligible |= eligible

    def schedule(self, start_time, id):
        job = self.prob.jobs[id]

        self.finish_time[id] = start_time + job.duration
        self.unprocessed.remove(id)
        self.scheduled.add(id)

        for j in job.successors:
            self.prob.jobs[j].in_degree -= 1

    def calc_remaining(self, t):
        remaining = copy(self.prob.resources)
        for j in self.active_jobs(t):
            remaining = [a - b for a, b in zip(remaining, j.resources)]
        return remaining

    def active_jobs(self, t):
        active = set()
        for j in self.prob.jobs:
            if t < self.finish_time[j.id] and self.finish_time[j.id] - j.duration <= t:
                active.add(j)
        return active

    def select(self):
        return self.eligible.pop()

    def backward_pass(self):
        q = queue.SimpleQueue()
        jobs = deepcopy(self.prob.jobs)

        # Total sum of job durations works as an upperbound
        upper_bound = sum([job.duration for job in self.prob.jobs])

        self.latest_finish = [upper_bound] * self.prob.njobs
        self.latest_start = [-1] * self.prob.njobs

        q.put(jobs[-1])
        self.latest_start[-1] = upper_bound

        while q.empty() == False:
            job = q.get()
            t = self.latest_finish[job.id] - job.duration
            for j in job.predecessors:
                pred = jobs[j]
                if self.latest_finish[j] >= t:
                    self.latest_finish[j] = t
                    self.latest_start[j] = t - pred.duration
                pred.nsuccessors -= 1
                if pred.nsuccessors == 0:
                    q.put(pred)


def is_resource_feasible(job, remaining):
    return all([r <= R for (r, R) in zip(job.resources, remaining)])


def sgs(prob):
    sol = Solution(prob)

    # Calculate LF for this instance
    sol.backward_pass()
    
    # Insert dummy start job
    sol.schedule(id=0, start_time=0)

    for i in range(1, prob.njobs):
        print(f"Stage {i}")

        # Calculate eligible jobs
        sol.calc_eligible()
        print(f"D_g = {sol.eligible}")

        # Get the finish times of eligible jobs
        finish_times = [sol.finish_time[j] for j in sol.scheduled]
        print(f"F_g = {finish_times} ")

        # Calculate remaining resource capacities
        remaining = {}
        for t in finish_times:
            remaining[t] = sol.calc_remaining(t)
            print(f"~R({t}) = {remaining[t]}")

        # Select one job
        j = sol.select()
        job = sol.prob.jobs[j]
        print(f"j = {j}")

        # Calculate EF
        EF = max([sol.finish_time[h] for h in job.predecessors]) + job.duration
        LF = sol.latest_finish[j]
        print(f"EF_j = {EF}; LF_j = {LF}")

        # Calculate all times with resource feasibility    
        possible_times = [t for t in range(EF - job.duration, LF - job.duration) if t in finish_times]
        feasible_times = []
        for t in possible_times:
            taus = [tau for tau in range(t, t + job.duration) if tau in finish_times]
            if all([is_resource_feasible(job, remaining[tau]) for tau in taus]):
                feasible_times.append(t)

        print(f"Possible times = {possible_times}")
        print(f"Feasible times = {feasible_times}")

        start = min(feasible_times)

        # Add job to solution
        sol.schedule(start, j)
        print(f"Scheduled {j} at {start}")
        print("---------------------------------")

    return sol
    
if __name__ == "__main__":
    file = "data/j30/j301_1.sm"
    if len(sys.argv) > 1:
        file = sys.argv[1]
    prob = read_file(file)
    sol  = sgs(prob)

    print(sol.finish_time)
