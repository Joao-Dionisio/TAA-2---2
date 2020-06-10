'''
 Here we implemented beam search. Like complete search, but we only pursuit those solutions
 whose fitness is at least as good as the minimum one. We set the number of solutions we 
 pursuit to n_solutions and we keep looking at other possible solutions. If they are more
 promissing, then those are the ones that we'll pursue. 
 '''

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

class candidateSolutions:

    def __init__(self):
        self.candidate_solutions = []
        

    def calculate_worst_solution(self):
        worst_child = self.candidate_solutions[0]
        worst_index = 0
        for index, child in enumerate(self.candidate_solutions):
            if child.solution_fitness < worst_child.solution_fitness:
                worst_child = child
                worst_index = index
        self.worst_child = worst_child
        self.worst_index =  worst_index

    def replace(self, new_child):
        self.candidate_solutions[self.worst_index] = new_child
        self.calculate_worst_solution() 

def start_beam_search(file, n_solutions):
    prob = read_file(file)
    sol = completeSearchSolution(prob)
    sol.backward_pass()
    sol.schedule(id=0, start_time=0)
    sol.calc_solution_fitness()
    beam_search(sol, n_solutions)
    
    print([i.finish_time for i in beamSearch.candidate_solutions])
    min = float('inf')
    for i in beamSearch.candidate_solutions:
        if max(i.finish_time) < min:
            min = max(i.finish_time)
    return min



def beam_search(parent_solution, n_solutions):
    parent_solution.calc_eligible()
    improved_this_round = [0] * n_solutions
    
    l = len(parent_solution.eligible)
    

    best_temp_sol = None

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
        
        temp_sol.calc_solution_fitness()
        if len(beamSearch.candidate_solutions) < n_solutions:
            beamSearch.candidate_solutions.append(temp_sol)
            beamSearch.calculate_worst_solution() # Just to initialize worst_child and worst_index variables
            improved_this_round[len(beamSearch.candidate_solutions)-1] = 1
            beam_search(temp_sol, n_solutions)
        else:
            # Maybe store the solution fitness?
            if temp_sol.solution_fitness > beamSearch.worst_child.solution_fitness:
                improved_this_round[beamSearch.worst_index] = 1
                beamSearch.replace(temp_sol)
            else:
                if best_temp_sol == None:
                    best_temp_sol = temp_sol
                elif temp_sol.solution_fitness > best_temp_sol.solution_fitness:
                    best_temp_sol = temp_sol
                
                
    if 1 not in improved_this_round:
        if len(parent_solution.eligible) > 0:
            new_index = beamSearch.candidate_solutions.index(parent_solution) 
            beamSearch.candidate_solutions[new_index]= best_temp_sol # If no improvement is found, just continue search using the best solution found
            improved_this_round[new_index] = 1
        
    for index in range(len(improved_this_round)):
        if improved_this_round[index] == 1:
            beam_search(beamSearch.candidate_solutions[index], n_solutions) 

    
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

'''
if __name__ == "__main__":
    file = "data/j30/j301_1.sm"
    if len(sys.argv) > 1:
        file = sys.argv[1]
    start_beam_search(file, 15)
'''

if __name__ == "__main__":
    results = []
    for i in range(1, 49):
        global beamSearch
        beamSearch = candidateSolutions()
        file = "data/j30/j30" + str(i) + "_1.sm"
        prob = read_file(file)
        sol  = start_beam_search(file,5)
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
