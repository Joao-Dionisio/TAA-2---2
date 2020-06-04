import sys
import queue
from copy import copy, deepcopy

from data import *


class Solution:
    def __init__(self, prob):
        self.prob = deepcopy(prob)

        # array of int indexed by job id
        self.finish_time = [0] * prob.njobs

        self.earliest_start  = [0] * prob.njobs
        self.earliest_finish = [0] * prob.njobs
        self.latest_start    = [0] * prob.njobs
        self.latest_finish   = [0] * prob.njobs

        self.duration = 0

        # set of scheduled job ids
        self.scheduled = set()

        # set of jobs that can be scheduled
        self.eligible = set()

        # set of unprocessed jobs
        self.unprocessed = [i for i in range(0, prob.njobs)]


    def calc_eligible(self):
        eligible = set()

        for j in self.unprocessed:
            job = self.prob.jobs[j]
            if (job.is_ready()):
                eligible.add(j)

        self.eligible |= eligible

    def schedule(self, start_time, id):
        job = self.prob.jobs[id]

        self.finish_time[id] = start_time + job.duration
        self.unprocessed.remove(id)
        self.scheduled.add(id)

        for j in job.successors:
            self.prob.jobs[j].in_degree -= 1
            self.prob.jobs[j].earliest_start = max(
                self.prob.jobs[j].earliest_start,
                start_time + job.duration)

    def calc_remaining(self, t):
        remaining = copy(self.prob.resources)
        active = self.active_jobs(t)
        for j in active:
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

        # job = -1
        # max_d = 999999
        # for j in self.eligible:
        #     if self.prob.jobs[j].duration < max_d:
        #         max_d = self.prob.jobs[j].duration
        #         job = j
            
        # max_r = 9999999
        # job = -1
        # for j in self.eligible:
        #     r = sum(self.prob.jobs[j].resources)
        #     if r < max_r:
        #         job = j
        #         max_r = r

        # self.eligible.remove(job)
        # return job

    def forward_pass(self):
        q = queue.SimpleQueue()
        jobs = deepcopy(self.prob.jobs)

        q.put(jobs[0])

        while(q.empty() == False):
            job = q.get()
            t = self.earliest_start[job.id] + job.duration
            for j in job.successors:
                succ = jobs[j]
                if (self.earliest_start[j] <= t):
                    self.earliest_start[j] = t
                    self.earliest_finish[j] = t + succ.duration
                succ.in_degree -= 1
                if succ.is_ready():
                    q.put(succ)

        self.duration = self.earliest_finish[-1]

    def backward_pass(self):
        q = queue.SimpleQueue()
        jobs = deepcopy(self.prob.jobs)

        upper_bound = sum([job.duration for job in self.prob.jobs])

        #self.latest_finish = [self.duration] * self.prob.njobs
        self.latest_finish = [upper_bound] * self.prob.njobs
        self.latest_start = [-1] * self.prob.njobs

        q.put(jobs[-1])
        self.latest_start[-1] = self.duration

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

def is_feasible(job, remaining):
    result = True
    for (r, R) in zip(job.resources, remaining):
        result = result and r <= R
    return result


def sgs(prob):
    sol = Solution(prob)

    sol.forward_pass()
    sol.backward_pass()
    
    # print(f"ES {sol.earliest_start}")
    # print(f"EF {sol.earliest_finish}")
    # print(f"LS {sol.latest_start}")
    # print(f"LF {sol.latest_finish}")

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
        print(f"EF_j = {EF} or {job.earliest_start + job.duration} or {sol.earliest_finish[j]}")
        print(f"LF_j = {LF}")

        # Calculate finish time of job
        #sol.finish_time[j] = min

        # print("-------feasibility-------")
        print(job.resources)
        possible_times = [t for t in range(EF - job.duration, LF - job.duration) if t in finish_times]
        feasible_times = []
        for t in possible_times:
            # print(f"t = {t}")
            taus = [tau for tau in range(t, t + job.duration) if tau in finish_times]
            # print(f"taus: {taus}")
            feasible = True
            for tau in taus:
                feasible = feasible and is_feasible(job, remaining[tau])
            if feasible:
                feasible_times.append(t)
        # print("------------------------")

        print(f"Possible times = {possible_times}")
        print(f"Feasible times = {feasible_times}")

        # delete when fixed
        # if feasible_times == []: feasible_times = [sol.earliest_start[j]]

        start = min(feasible_times)
        # sol.finish_time[j] = start + job.duration

        # Add job to solution
        sol.schedule(start, j)
        print(f"Scheduled {j} at {start}")

        print("---------------------------------")

    # for j in sol.prob.jobs:
    #     print(j.earliest_start)

    print(sol.finish_time)
    print(len(sol.finish_time))
    # print(sol.prob.jobs[-1].earliest_start)
    
if __name__ == "__main__":
    file = "data/j30/j301_1.sm"
    if (len(sys.argv) > 1):
        file = sys.argv[1]
    prob = read_file(file)
    sgs(prob)
