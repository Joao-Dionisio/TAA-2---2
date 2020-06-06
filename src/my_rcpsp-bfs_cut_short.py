'''

So, the idea is:


you take the sgs solution 


and you adapt the algorithm. Instead of trying to decide which is the best solution,
you instead try all of them. This will result in a really big tree, so we decided to
do beam search.
'''
from copy import copy
from my_sgs import *
import gc


class solutionTree:
    def __init__(self):
        self.admissible_solutions = []


def start_complete_search(file, n_levels):
    prob = read_file(file)
    global completeSearch
    completeSearch = []
    sol = Solution(prob)
    sol.backward_pass()
    sol.schedule(id=0, start_time=0)
    complete_search(sol, 0, n_levels)
    possible_solutions = []
    print(len(completeSearch))
    for i in completeSearch:
        possible_solutions.append(get_solution(i))
    print([max(i.finish_time) for i in possible_solutions])

def complete_search(parent_solution, recursion_level, n_levels):
    #print(parent_solution.eligible)
    parent_solution.calc_eligible()
    #print(parent_solution.eligible)
    if recursion_level < n_levels:
        while len(parent_solution.eligible) > 0:
            temp_sol = copy(parent_solution)
            finish_times = [temp_sol.finish_time[j] for j in temp_sol.scheduled]
            remaining = {}
            for t in finish_times:
                remaining[t] = temp_sol.calc_remaining(t)
            print(parent_solution.eligible)
            j = temp_sol.select() #asdjnasdjnas
            print(parent_solution.eligible)
            #parent_solution.select()
            '''if recursion_level != n_levels -1 :
                print(l-1)
                print(temp_sol.eligible)
            j = temp_sol.choose_job(temp_sol, l-1)'''
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
    if recursion_level == n_levels:
        completeSearch.append(parent_solution)
        return
    
    
def get_solution(sol):
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
    return sol
        



#import time

#b = start_complete_search(a[0], a[1], 'j3048_7.sm')
#sol = Solution()
#sol.best_F = run('j3048_7.sm')
#print(start_complete_search('j3048_7.sm'))

if __name__ == "__main__":
    file = "data/j30/j301_1.sm"
    if len(sys.argv) > 1:
        file = sys.argv[1]
    sol  = start_complete_search(file, 1)


'''x = 'j301_'
for i in range(1, 11):
    start = time.time()
    test = x + str(i) + '.sm'
    sol.best_F = run(test)
    print(sol.best_F)
    print(start_complete_search(test))
    print(time.time() - start)
'''
