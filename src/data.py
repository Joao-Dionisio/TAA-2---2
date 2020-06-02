class Job:
    def __init__(self):
        self.id = -1            # int
        self.duration = 0       # int
        self.resources = []     # array of int (resource id)
        self.nsucessors = 0     # int
        self.sucessors = []     # array of int (job id)
        self.predecessors = []  # array of int (job id)

    def __init__(self, id):
        __init__(self)
        self.id = id
        
    def __str__(self):
        return "Job {}\nduration: {}\nresources: {}\nsucessors: {}".format(
                    self.id, self.duration, self.resources, self.sucessors)


class Problem:
    def __init__(self):
        self.njobs = 0          # int
        self.jobs = []          # array of Job
        self.nresources = 0     # int
        self.resources = []     # array of Resource
        self.duedate = 0        # int

    def __str__(self):
        return "njobs:\t\t{}\nresources:\t{}\nduedate:\t{}\n".format(
                    self.njobs, self.resources, self.duedate)

def read_file(file):
    prob = Problem()

    with open(file, 'r') as f:
        lines           = f.readlines();

        prob.njobs      = int(lines[5].split(":")[1])
        prob.nresources = int(lines[8].split(":")[1].split()[0])
        prob.duedate    = int(lines[14].split()[3])

        rel_end_line   = read_relations(prob, lines, 18)
        stats_end_line = read_job_stats(prob, lines, rel_end_line + 5)

        l = lines[stats_end_line + 4].split()
        prob.resources = [int(r) for r in l]

        f.close()


def read_relations(prob, lines, job_start_line):
    job_end_line = job_start_line - 1 + prob.njobs

    for i in range(job_start_line, job_end_line):
        l = lines[i].split()
        job = Job()
        job.id         = int(l[0]) - 1
        job.nsucessors = int(l[2])
        job.sucessors  = [int(s) for s in l[-job.nsucessors:]]
        prob.jobs.append(job)
    
    prob.jobs.append(Job(prob.njobs - 1))
    
    return job_end_line

def read_job_stats(prob, lines, resource_start_line):
    resource_end_line = resource_start_line - 1 + prob.njobs

    for i in range(resource_start_line, resource_end_line):
        l = lines[i].split()
        id = int(l[0]) - 1
        prob.jobs[id].duration  = l[2]
        prob.jobs[id].resources = [int(r) for r in l[-prob.nresources:]]

    return resource_end_line