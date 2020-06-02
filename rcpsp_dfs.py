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



class Solution:

    # This should be unchanged
    def read_file():
        return

        
    class Resources:
        def __init__(self):
            self.number_of = -1
            self.max_capacity = []
            self.available_resources = {}

       # We are doing the same thing multiple times. Instead of scheduled_activities, we should only pass the most recent activity to be scheduled
        def calculate_resources(self, scheduled_activities):
            activity_intersections = resource_dependencies(scheduled_activities) # {finish_time_1: [r_1(1),...,r_k(1)], ... , finish_time_n: [r_1(n),...,r_k(n)]}
            for time in activity_intersections:
                for j in activity_intersections[time]:
                    #if time in resources.available_resources:
                    #    resources.available_resources[time] = [resources.available_resources[time][r_k] - j.required_resources[r_k] for r_k in range(resources.number_of)]
                    
                        self.available_resources[time] = [self.max_capacity[r_k] - j.required_resources[r_k] for r_k in range(self.number_of)]                    
            return self.available_resources



    class Activity:
        def __init__(self, information):
            self.id = information[0]  
            self.duration = information[1]
            self.required_resources = information[2]
            self.successors = [i for i in information[3]]
            self.predecessors = []
            self.scheduled = False
            self.start = None
            self.end = None #self.start + self.duration

        def calculate_precedents(self, activities):
            # I'm gonna assume no one's an asshole and that you can only be a successor of an activity with a lower number than yours
            predecessors = []
            for i in range(len(self.successors)):
                cur_predecessor = []
                for j in range(i):
                        if i in self.successors[j]:
                            cur_predecessor.append(j)
                predecessors.append(cur_predecessor)
            self.predecessors = predecessors



# best = float('inf') at the start



def complete_search(activities, resources, S, best):
    durations = [i.duration for i in activities]
    S = [activities[0]] # First dummy activity
    l = activities[-1].id
    F = (l+1)*[0]
    LF = calculate_latest_finish(activities)
    D = []
    activities[0].start = activities[0].end = 0 # dummy
    for i in range(l):
        
        resources.calculate_resources(S)
        D = calculate_eligible_activities(activities, resources)

        for j in D:
            # Divide into every possible branch
            a = complete_search(activities, resources, S)
            if a[0] < best:
                best = a[0]
                best_schedule = a[1]
        cur_activity = chosen_activity
             
    
        precedent_finish_times = [F[j.id] for j in cur_activity.predecessors] # YOU ARE HERE RIGHT NOW
        if precedent_finish_times == []:
            precedent_finish_times = [0]
        EF = max(precedent_finish_times) + cur_activity.duration # We only need EF_{j} for iteration j
        print(cur_activity.id)
        possible_times = calculate_possible_times(cur_activity, resources, F, EF)
        cur_activity.start = min(possible_times)
        cur_activity.end = cur_activity.start + cur_activity.duration
        
        
        F[cur_activity.id] = cur_activity.end
        cur_activity.scheduled = True
        if chosen_activity.id != 0:
            S.append(chosen_activity)
        if i < l-1:
            D.remove(chosen_activity)
                
    F[-1] = max(F) # The last activity will be a precedent of activity n
    print(F)
    return [F[-1], [activities, resources]]



# Performs a DFS on all possible solutions
def complete_search(activities, resources, ):
    eligible_activities = calculate_eligible_activities(activities, resources)
    for i in eligible_activities:
        cur_time = min(calculate_possible_times(activities, i, resources, F, EF))
        if cur_time + i.duration < best_so_far:
            cur_F = F
            cur_F[i.id] = cur_time + i.duration
            # WE NEED TO UPDATE THE RESOURCES
            cur_resources = copy(resources)
            for i in cur_resources:
                if i > cur_time and i < cur_time + i.duration:
                    for j in resources.number_of:
                        cur_resources[i][j]-=i.required_resources[j]
            x[-1] = complete_search(activities, cur_resources, cur_F)
            if cur_F[-1] < best_F[-1]:
                best_F = cur_F
    return best_F


def add_activity(scheduled_activities, cur_activity, F):
    a = calculate_possible_times(scheduled_activities, cur_activity)
    F[cur_activity.id] = min(a) + cur_activity.duration
    return F



# We need to be careful with resources and activities
def calculate_possible_times(activities, cur_activity, resources, F, EF):
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



def caclulate_schedule(activities, resources, S):
    
    return

