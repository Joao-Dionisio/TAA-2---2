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


def start_complete_search(prob, n_levels):
    #prob = read_file(file)
    sol = Solution(prob)
    sol.backward_pass()
    sol.schedule(id=0, start_time=0)
    complete_search(sol, 0, n_levels)
    possible_solutions = []
    #print(len(completeSearch))
    for i in completeSearch:
        possible_solutions.append(get_solution(i))
    #print([i.finish_time for i in possible_solutions])
    min = float('inf')
    for i in possible_solutions:
        if max(i.finish_time) < min:
            min = max(i.finish_time)
    #print(min)
    return min

def complete_search(parent_solution, recursion_level, n_levels):
    parent_solution.calc_eligible()
    if recursion_level < n_levels:
        l = len(parent_solution.eligible)
        #while len(parent_solution.eligible) > 0:
        for z in range(l):
            temp_sol = deepcopy(parent_solution)
            finish_times = [temp_sol.finish_time[j] for j in temp_sol.scheduled]
            remaining = {}
            for t in finish_times:
                remaining[t] = temp_sol.calc_remaining(t)
            j = temp_sol.select(z) 
    
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
        
        j = sol.select(0)
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

'''
if __name__ == "__main__":
    file = "data/j30/j301_1.sm"
    if len(sys.argv) > 1:
        file = sys.argv[1]
    sol  = start_complete_search(file, 1)'''

if __name__ == "__main__":
    results = []
    for i in range(1, 49):
        global completeSearch
        completeSearch = []
        file = "data/j30/j30" + str(i) + "_1.sm"
        prob = read_file(file)
        sol  = start_complete_search(prob,6)
        print("j30" + str(i) + "_1.sm done!")

        results.append(sol)
    print(results)
    print(sum(results))


'''x = 'j301_'
for i in range(1, 11):
    start = time.time()
    test = x + str(i) + '.sm'
    sol.best_F = run(test)
    print(sol.best_F)
    print(start_complete_search(test))
    print(time.time() - start)
'''
