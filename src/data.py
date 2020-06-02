import copy

class Job:
    def __init__(self, id):
        self.id = id
        self.duration = 0     # int
        self.resources = []   # array of int (resource id)
        self.nsuccessors = 0  # int
        self.successors = []  # array of int (job id)
        self.ready = 0        # ready == 0 when all predecessors are complete
        
    def __str__(self):
        return "Job {}\nduration: {}\nresources: {}\nsuccessors: {}\nready:{}".format(
                    self.id, self.duration, self.resources, self.successors, self.ready)


class Problem:
    def __init__(self):
        self.njobs = 0          # int
        self.jobs = []          # array of Job
        self.nresources = 0     # int
        self.resources = []     # resources[i] = capacity of resource i

        # switch to struct-of-arrays if original solution is too slow        
        # self.durations      = [] # durations[j] = duration of job j
        # self.resource_uses  = [] # resource_uses[j] = resource usage of job j
        # self.nsuccessors    = [] # nsucessors[j] = number of successors for job j
        # self.successors     = [] # sucessors[j] = list of successors of job j
        # self.ready          = [] # ready[j] == 0 if all predecessors of j are completed

    def __str__(self):
        return "njobs:\t\t{}\nresources:\t{}\n".format(
                    self.njobs, self.resources)

def read_file(file):
    prob = Problem()

    with open(file, 'r') as f:
        lines           = f.readlines();

        prob.njobs      = int(lines[5].split(":")[1])
        prob.nresources = int(lines[8].split(":")[1].split()[0])

        rel_end_line   = read_relations(prob, lines, 18)
        stats_end_line = read_job_stats(prob, lines, rel_end_line + 5)

        l = lines[stats_end_line + 4].split()
        prob.resources = [int(r) for r in l]

        f.close()
    
    return prob


def read_relations(prob, lines, job_start_line):
    job_end_line = job_start_line - 1 + prob.njobs

    for i in range(job_start_line, job_end_line):
        l = lines[i].split()
        job            = Job(int(l[0]) - 1)
        job.nsuccessors = int(l[2])
        job.successors  = [int(s) - 1 for s in l[-job.nsuccessors:]]
        prob.jobs.append(job)
    
    prob.jobs.append(Job(prob.njobs - 1))
    
    for j in prob.jobs:
        for succ in j.successors:
            prob.jobs[succ].ready += 1

    return job_end_line

def read_job_stats(prob, lines, resource_start_line):
    resource_end_line = resource_start_line - 1 + prob.njobs

    for i in range(resource_start_line, resource_end_line):
        l = lines[i].split()
        id = int(l[0]) - 1
        prob.jobs[id].duration  = l[2]
        prob.jobs[id].resources = [int(r) for r in l[-prob.nresources:]]

    return resource_end_line