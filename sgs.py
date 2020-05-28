# We need to check what the input is

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
                
                    resources.available_resources[time] = [resources.max_capacity[r_k] - j.required_resources[r_k] for r_k in range(resources.number_of)]                    
        return resources.available_resources



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


        
    



def read_file(file):

    # This is so much data wtf
    # For now, let's deliver the data like
    #[..., [activity i, duration, [resources], [sucecessors]], ....]
    # So, for jobnr. 1 of j30 of the first dataset we have
    # [[1, 0, [0,0,0,0], [2,3,4]], [2, 2, [1,2,4,0], [10,11,28]], ... ]
    activities = [Activity(information)]
    for i in activities:
        i.calculate_precedents()
    resources = Resources()
    resources.max_capacity = asokdmasoadsomdIJSDNFIJNDSFIJSasipoads # Reading the file
    resources.available_resources = resources.max_capacity
    resources.number_of = len(resources.available_resources)
    return [activities, resources]



        

def sgs(activities, resources):
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

        chosen_activity = D[0] 
        chosen_resources = sum(chosen_activity.required_resources)
        for j in D:
            if sum(j.required_resources) > chosen_resources: # We choose the activity that takes the most resources
                chosen_activity = j
        cur_activity = chosen_activity
        
        '''earliest_start = float('inf')
        for cur_activity in D:
            cur_earliest_start = float('inf')
            for h in resources.available_resources:
                if all(cur_activity.required_resources[z] <= resources.available_resources[h][z] for z in range(resources.number_of)):
                            cur_earliest_start = h
                            break
            if cur_earliest_start < earliest_start:
                earliest_start = cur_earliest_start
                chosen_activity = cur_activity'''
     
    
        precedent_finish_times = [F[j.id] for j in cur_activity.predecessors] # YOU ARE HERE RIGHT NOW
        if precedent_finish_times == []:
            precedent_finish_times = [0]
        EF = max(precedent_finish_times) + cur_activity.duration # We only need EF_{j} for iteration j
        print(cur_activity.id)
        possible_times = calculate_possible_times(cur_activity, F, EF)
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
    return F[-1]





def calculate_latest_finish(activities):
    
    return

                
def calculate_possible_times(cur_activity, F, EF):
    j = cur_activity.id
    LF = 1000 # delete this later, should be an argument
    initial_times = [i for i in F if i >= EF - cur_activity.duration and i <= LF - cur_activity.duration] # This is just that big train in the paper

    possible_times = []    
    for t in initial_times:
        if all(cur_activity.required_resources[i] <=  resources.available_resources[t][i] for i in range(resources.number_of)):
            possible_times.append(t)

    #if cur_activity.id == 3:
    #    print(initial_times)
    
    if initial_times == []:
        possible_times = [max(F)] 

    if possible_times == []:
        possible_times = [max(initial_times)]
    
    

    return possible_times



def calculate_eligible_activities(activities, resources):
    n_resources = resources.number_of
    unscheduled_activities = [i for i in activities if i.scheduled == False]
    # removing unscheduled activities whose precedents haven't been scheduled.
    to_remove = []
    for i in unscheduled_activities:
        for j in i.predecessors:
            if j.scheduled == False:
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
    return eligible_activities




def resource_dependencies(activities):
    dic = {}
    #activities = [[i.start, i.start + i.duration] for i in activities]
    for i in activities:
        if i.start + i.duration not in dic:
            dic[i.start + i.duration] = []
    for i in activities:
        for j in dic:
            if i.start <= j and i.start+i.duration >= j:
                dic[j].append(i)
    return dic







def calculate_precedents(activities):
    predecessors = []
    ids = [i.id for i in activities]
    for i in activities:
        for j in i.successors:
            activities[ids.index(j)].predecessors.append(i)
            
    


a = Activity([0,0,[0],[1,2]])
b = Activity([1,3,[2],[3]])
c = Activity([2,4,[3],[4]])
d = Activity([3,2,[4],[5]])
e = Activity([4,2,[4],[6]])
f = Activity([5,1,[3],[7]])
g = Activity([6,4,[2],[7]])
h = Activity([7,0,[0],[]])
activities = [a,b,c,d,e,f,g,h]
resources = Resources()
resources.number_of = 1
resources.max_capacity = [4]
resources.available_resources = {0: [4]}
calculate_precedents(activities)
sgs(activities, resources)


'''
a = Activity([0,0,[0,0],[1,2]])
b = Activity([1,3,[2,1],[3]])
c = Activity([2,4,[2,1],[3,4]])
d = Activity([3,6,[2,1],[5]])
e = Activity([4,2,[2,1],[5,6]])
f = Activity([5,1,[3,0],[7]])
g = Activity([6,4,[3,1],[7]])
h = Activity([7,0,[0,0],[]])
activities = [a,b,c,d,e,f,g,h]
resources = Resources()
resources.number_of = 2
resources.max_capacity = [4,2]
resources.available_resources = {0: [4,2]} 
calculate_precedents(activities)
sgs(activities, resources) 
'''

for i in resources.available_resources:
    if not all(resources.available_resources[i][k] >= 0 for k in range(resources.number_of)):
        print('False')
