'''

So, the idea is:


you take the sgs solution 


and you adapt the algorithm. Instead of trying to decide which is the best solution,
you instead try all of them. This will result in a really big tree, so we need
to branch and bound.

We should do a dfs in order to increase chances of pruning. It will basically be BB

For every algo to bin packing, we also have an algo for this algorithm.
The things we put in the bins are the tasks, and they have r + 1 dimensions,
where r is the number of resources, plus 1 which corresponds to the duration.
It's easier to explain with an example.
Suppose task 1 demands [3,1,2] resources and takes 5 to complete.
So we imagine task 1 as a 3x1x2x5 box that we need to pack.

Doing this, we can imagine that we're packing items one next to another iff
there's space left, and that only happens if the resource needed are smaller than

'''
from copy import copy
from sgs import *
import gc


class Solution:
    def __init__(self):
        self.best_F = 33*[float('inf')]

def start_complete_search(activities, resources, file):
    sol = Solution()
    sol.best_F = run(file)
    print(sol.best_F)
    S = (len(activities)+1)*[0]
    S[0] = 1
    S[1] = 1
    return complete_search(activities, resources, S, (len(activities)+1)*[0], sol.best_F, 0)


# Performs a DFS on all possible solutions
def complete_search(activities, resources, S, F, best_F, recursion_level):
    #print(F)
    eligible_activities = calculate_eligible_activities_2(activities, resources, S)
    l = len(eligible_activities)
    for j in range(l):
        i = eligible_activities[j]
        precedent_finish_times = [F[j.id] for j in i.predecessors]
        EF = max(precedent_finish_times) + i.duration
        cur_time = min(calculate_possible_times_2(activities, i, resources, F, EF))
        if cur_time + i.duration < best_F[-1]:
            cur_F = F
            cur_F[i.id] = cur_time + i.duration
            cur_resources = copy(resources)
            for k in cur_resources.available_resources:
                if k > cur_time and k < cur_time + i.duration:
                    for j in range(resources.number_of):
                        cur_resources[k][j]-=i.required_resources[j]
            cur_S = copy(S)
            cur_S[i.id] = 1
            if 0 in cur_S[2:]:
                if recursion_level < 6:
                    complete_search(activities, cur_resources, cur_S, cur_F, sol.best_F, recursion_level+1)
                else:
                    cur_F = find_solution(activities, cur_resources, cur_S, cur_F)
                    S = (len(activities)+1)*[1]
            #print(sol.best_F)
            #print(cur_F)
            #print(i)
            if cur_F[-1] < sol.best_F[-1] and 0 not in S:
                #print('asd')
                sol.best_F = cur_F
        gc.collect()
    return sol.best_F


def find_solution(activities, cur_resources, S, cur_F):
    while 0 in S[:-1]:
        eligible_activities = calculate_eligible_activities_2(activities, cur_resources, S)
        chosen_activity = eligible_activities[0]
        chosen_resources = sum(chosen_activity.required_resources)
        for j in eligible_activities:
            if sum(j.required_resources) > chosen_resources:
                chosen_activity = j
        cur_activity = chosen_activity
        precedent_finish_times = [cur_F[j.id] for j in cur_activity.predecessors]
        EF = max(precedent_finish_times) + cur_activity.duration
        #possible_times = min(calculate_possible_times_2(cur_activity, cur_resources, cur_F, EF))
        cur_time = min(calculate_possible_times_2(activities, cur_activity, cur_resources, cur_F, EF))
        cur_F[cur_activity.id] = cur_time + cur_activity.duration
        S[cur_activity.id] = 1
    cur_F[-1] = max(cur_F)
    S[-1] = 1
    return cur_F
    

#WE ARE ASSUMING THAT, BESIDES ACTIVITY 0 (AND -1), THERE ARE NO ACTIVITIES WITH DURATION 0
def calculate_eligible_activities_2(activities, resources, cur_S):
    n_resources = resources.number_of
    unscheduled_activities = [i for i in activities if cur_S[i.id] == 0] # The unscheduled activities are the ones that aren't in S. Activity 0 ends at 0, so it's discarded
    # removing unscheduled activities whose precedents haven't been scheduled.
    to_remove = []
    for i in unscheduled_activities:
        for j in i.predecessors:
            if cur_S[j.id] == 0: 
                to_remove.append(i)
                break
    unscheduled_activities = [i for i in unscheduled_activities if i not in to_remove]
    eligible_activities = []
    for cur_activity in unscheduled_activities:
        for t in resources.available_resources:
            if all(cur_activity.required_resources <= resources.available_resources[t] for i in range(resources.number_of)):
                cur_activity.start = t # I am not sure about this
                cur_activity.end = cur_activity.start + cur_activity.duration 
                eligible_activities.append(cur_activity)

    if eligible_activities == []:
        chosen_activity = unscheduled_activities[0]
        chosen_resources = sum(chosen_activity.required_resources) 
        for i in unscheduled_activities:
            if sum(i.required_resources) > chosen_resources:
                chosen_activity = i
        eligible_activities.append(chosen_activity)
    #print([i.id for i in unscheduled_activities])
    #print([i.id for i in eligible_activities])    
    return eligible_activities



# We need to be careful with resources and activities
def calculate_possible_times_2(activities, cur_activity, resources, F, EF):
    j = cur_activity.id
    LF = 1000 # delete this later, should be an argument
    initial_times = [i for i in F if i >= EF - cur_activity.duration and i <= LF - cur_activity.duration] # This is just that big train in the paper

    possible_times = []    
    for t in initial_times:
        if all(cur_activity.required_resources[i] <=  resources.available_resources[t][i] for i in range(resources.number_of)):
            possible_times.append(t)
    
    if initial_times == []:
        possible_times = [max(F)] 

    if possible_times == []:
        possible_times = [max(initial_times)]
    
    return possible_times


sol = Solution()
a = read_file('j3048_7.sm')
b = start_complete_search(a[0], a[1], 'j3048_7.sm')

if b != sgs(a[0], a[1]):
    print('asdasd')
