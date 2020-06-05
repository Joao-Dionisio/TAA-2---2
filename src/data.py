class Job:
    def __init__(self, id):
        self.id = id
        self.duration = 0        # int
        self.resources = []      # array of int (resource id)
        self.nsuccessors = 0     # int
        self.successors = []     # array of int (job id)
        self.npredecessors = 0   # int
        self.predecessors = []   # array of int (job id)
        self.in_degree = 0       # int
        self.earliest_start = 0  # int

    def is_ready(self):
        return self.in_degree == 0

    def __str__(self):
        return "Job {}\nduration: {}\nresources: {}\nsuccessors: {}\npredecessors: {}\nin_degree:{}".format(
            self.id, self.duration, self.resources, self.successors, self.predecessors, self.in_degree)


class Problem:
    def __init__(self):
        self.njobs = 0           # int
        self.jobs = []           # array of Job
        self.nresources = 0      # int
        self.resources = []      # resources[i] = capacity of resource i

    def __str__(self):
        return "njobs:\t\t{}\nresources:\t{}\n".format(self.njobs, self.resources)


def read_file(filename):
    try:
        f = open(filename, 'r')
    except IOError:
        print("file", filename, "could not be read")
        exit(-1)

    prob = Problem()
    lines = f.readlines()
    f.close()

    prob.njobs = int(lines[5].split(":")[1])
    prob.nresources = int(lines[8].split(":")[1].split()[0])

    rel_end_line = read_relations(prob, lines, 18)
    stats_end_line = read_job_stats(prob, lines, rel_end_line + 5)

    l = lines[stats_end_line + 4].split()
    prob.resources = [int(r) for r in l]


    calc_predecessors(prob)

    return prob


def read_relations(prob, lines, job_start_line):
    job_end_line = job_start_line - 1 + prob.njobs

    for i in range(job_start_line, job_end_line):
        l = lines[i].split()
        job = Job(int(l[0]) - 1)
        job.nsuccessors = int(l[2])
        job.successors  = [int(s) - 1 for s in l[-job.nsuccessors:]]
        prob.jobs.append(job)

    prob.jobs.append(Job(prob.njobs - 1))

    for j in prob.jobs:
        for succ in j.successors:
            prob.jobs[succ].in_degree += 1

    return job_end_line


def read_job_stats(prob, lines, resource_start_line):
    resource_end_line = resource_start_line - 1 + prob.njobs

    for i in range(resource_start_line, resource_end_line):
        l = lines[i].split()
        id = int(l[0]) - 1
        prob.jobs[id].duration = int(l[2])
        prob.jobs[id].resources = [int(r) for r in l[-prob.nresources:]]

    return resource_end_line


def calc_predecessors(prob):
    for job in prob.jobs:
        for j in job.successors:
            prob.jobs[j].predecessors.append(job.id)

