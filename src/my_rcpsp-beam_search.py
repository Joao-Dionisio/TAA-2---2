'''
Com o beam search não estou a ver como o fazer.
Aquilo que estava a tentar era ter um número n_solutions de possíveis soluções parciais
a cada instante, e em cada iteração, se houver uma solução parcial que resulte
numa maior fitness, então substitui a solução que tem menor fitness. Não estou a conseguir
fazer com que isto aconteça até a solução parcial se tornar numa solução completa.

A fitness de uma solução é dada como o inverso do tempo final que obtemos quando forçamos
uma solução parcial a dar uma solução completa, através do sgs.
'''
from copy import copy
from my_sgs import *
import gc

class completeSearchSolution(Solution):
    
    # Calculates the fitness of a solution, bassed on the time provided by sgs
    def calc_solution_fitness(self):
        temp_sol = deepcopy(self)
        solution_fitness = max(get_solution(temp_sol).finish_time)
        self.solution_fitness = 1/solution_fitness


def start_beam_search(file, n_solutions):
    prob = read_file(file)
    global beamSearch
    beamSearch = []
    sol = completeSearchSolution(prob)
    sol.backward_pass()
    sol.schedule(id=0, start_time=0)
    sol.calc_solution_fitness()
    beam_search(sol, n_solutions)
    print(len(beamSearch))
    
    print([i.finish_time for i in beamSearch])
    min = float('inf')
    for i in beamSearch:
        if max(i.finish_time) < min:
            min = max(i.finish_time)
    print(min)

def beam_search(parent_solution, n_solutions):
    parent_solution.calc_eligible()
    
    improvement = 0
    
    while len(parent_solution.eligible) > 0:
        temp_sol = deepcopy(parent_solution)
        finish_times = [temp_sol.finish_time[j] for j in temp_sol.scheduled]
        remaining = {}
        for t in finish_times:
            remaining[t] = temp_sol.calc_remaining(t)
        j = temp_sol.select() 
        parent_solution.select()

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
        #print(len(temp_sol.eligible))
        temp_sol.calc_solution_fitness()
        if len(beamSearch) < n_solutions:
            improvement = 1
            beamSearch.append(temp_sol)
            beam_search(temp_sol, n_solutions)
        else:
            worst_child = beamSearch[0]
            worst_index = 0
            for index, child in enumerate(beamSearch):
                if child.solution_fitness < worst_child.solution_fitness:
                    worst_child = child
                    worst_index = index
            if temp_sol.solution_fitness > worst_child.solution_fitness:
                worst_child = temp_sol
                improvement = 1
    if improvement == 0:
        if len(parent_solution.eligible) > 0:
            worst_child = temp_sol
        else:
            return
    if len(beamSearch) == n_solutions:
        beamSearch[worst_index] = worst_child
        beam_search(worst_child, n_solutions)
            
    
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
    sol  = start_beam_search(file, 2)


'''x = 'j301_'
for i in range(1, 11):
    start = time.time()
    test = x + str(i) + '.sm'
    sol.best_F = run(test)
    print(sol.best_F)
    print(start_complete_search(test))
    print(time.time() - start)
'''
