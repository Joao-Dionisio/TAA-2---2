# We need to check what the input is

class Resources:
    def __init__(self):
        self.number_of = -1
        self.max_capacity = []
        self.available_resources = {}


    # We don't need to know the activities in any point in time, just at the start of a given activity
    def calculate_resources(self, scheduled_activities):
        activity_intersections = resource_dependencies(scheduled_activities) # {finish_time_1: [r_1(1),...,r_k(1)], ... , finish_time_n: [r_1(n),...,r_k(n)]}
        for time in activity_intersections:
            for j in activity_intersections[time]:
                if time in resources.available_resources:
                    resources.available_resources[time] = [resources.available_resources[time][r_k] - j.required_resources[r_k] for r_k in range(resources.number_of)]
                else:
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
    #required_resources = [i.resources for i in activities]
    durations = [i.duration for i in activities]
    S = [activities[0]] # First dummy activity
    l = activities[-1].id
    F = l*[0]
    LF = calculate_latest_finish(activities)
    D = []
    activities[0].start = activities[0].end = 0 # dummy
    for i in range(l):
        print([i.id for i in S])
        resources.calculate_resources(S)
        #if len(D) == 0:     # We only need to calculate eligible activities if there are none left
        D = calculate_eligible_activities(activities, resources)
        cur_activity = D[0] # Select one j \in D_{g}. We default to the first one
        precedent_finish_times = [F[activities[j]] for j in cur_activity.predecessors]
        if precedent_finish_times == []:
            precedent_finish_times = [0]
        EF = max(precedent_finish_times) + cur_activity.duration # We only need EF_{j} for iteration j
        possible_times = calculate_possible_times(activities[i], F, EF)
        cur_activity.start = min(possible_times)
        cur_activity.end = cur_activity.start + cur_activity.duration

        print([j.id for j in D])
        
        F[cur_activity.id] = cur_activity.end
        cur_activity.scheduled = True
        if D[0].id != 0:
            S.append(D[0])
        if i < l-1: 
            D.pop(0) # We scheduled the first of the eligibles, so we can remove         
        print(F)
                
    F[-1] = max(F) # The last activity will be a precedent of activity n
    return F[-1]





def calculate_latest_finish(activities):
    
    return

                
def calculate_possible_times(cur_activity, F, EF):
    j = cur_activity.id
    LF = 1000 # delete this later, should be argument
    initial_times = [i for i in F if i >= EF - cur_activity.duration and i <= LF - cur_activity.duration] # This is just that big train in the paper
    possible_times = []
    '''for t in initial_times:
        impossible = 0
        for resource in resources:
            for time in range(t, t + activity.duration):
                if available_resources[time] < resource[j][k]:
                    impossible = 1
                    break
            if impossible == 1:
                break
        if impossible == 0:
            possible_times.append(t)'''

    
    for t in initial_times:
        if all(cur_activity.required_resources[i] <  resources.available_resources[t][i] for i in range(resources.number_of)):
            possible_times.append(t)

    # YOU HAVE TO WORK HERE. 
    if possible_times == []:
        possible_times = [max(initial_times)+1]
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
            if all(cur_activity.required_resources < resources.available_resources[t] for i in range(resources.number_of)):
                cur_activity.start = t # I am not sure about this
                cur_activity.end = cur_activity.start + cur_activity.duration
                eligible_activities.append(cur_activity)
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


'''
def calculate_resources(activities):
    dic = {}
    activities = [[i.start, i.start + i.duration] for i in activities]
    for i in activities:
        if i.start + i.duration not in dic:
            dic[i.start + i.duration] = resources.max_capacity

    for i in activities:
        for j in dic:
            if i.start <= j and i.start+i.duration >= j:
                dic[j] = [dic[j][k] - i.required_resources[k] for k in range(resources.size_of)]
    return dic
'''




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
sgs(activities, resources)
