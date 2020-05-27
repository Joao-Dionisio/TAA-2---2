# We need to check what the input is

class Resources:
    def __init__(self):
        self.number_of = []
        self.max_capacity = []
        self.available_resources = []

    def calculate_resources(active_activities):
        for activity in active_activities:
            for resource in range(self.number_of):
                self.available_resources[resource]-=activity.required_resources[resource]
        return available_resources



class Activity:
    def __init__(self, information):
        self.id = information[0]
        self.duration = information[1]
        self.required_resources = information[2]
        self.successors = information[3]

    def calculate_precedents(self):
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

# We then feed read_file into sgs

def sgs(activities, resources):
    successors = [i.successors for i in activities]
    required_resources = [i.resources for i in activities]
    durations = [i.duration for i in activities]
    ids = [i.id for i in range(activities[-1].id)]
    #precedents = calculate_precedents(successors)
    S = [0] # First dummy activity
    l = ids[-1]
    F = l*[0]
    LF = calculate_latest_finish(activities)
    #active_activities = []
    for i in range(l):
        #R = calculate_resources(active_activities, available_resources)
        resources.calculate_resources()
        if len(D) == 0:     # We only need to calculate eligible activities if there are none left
            D = calculate_eligible_activities(active_activities, available_resources)
        cur_activity = activities[D[0]] # Select one j \in D_{g}
        precedent_finish_times = [F[activities[j]] for j in precedents[j]]
        EF = max(precedent_finish_times) + duration[j] # We only need EF_{j} for iteration j
        possible_times = calculate_possible_times(activities[i])
        F[j] = min(possible_times) + p[j]
        S.append(j)
        if i < l-1: 
            D = D[1:] # I think that if it doesn't pass this then it's impossible
            D.extend()
                
    F[-1] = max(F) # The last activity will be a precedent of activity n
    return F[-1]


'''
def calculate_precedents(successors):
    # I'm gonna assume no one's an asshole and that you can only be a successor of an activity with a lower number than yours
    predecessors = []
    for i in range(len(successors)):
        cur_predecessor = []
        for j in range(i):
                if i in successors[j]:
                    cur_predecessor.append(j)
        predecessors.append(cur_predecessor)
    return predecessors
'''

    
def calculate_variables(activities):

    return D, R

                
def calculate_latest_finish(activities):
    
    return

                
def calculate_possible_times(activity):
    initial_times = [i for i in F[:j] if i >= EF[j] - duration[j] and i <= LF[j] - duration[j]] # This is just that big train in the paper
    possible_times = []
    for t in initial_times:
        impossible = 0
        for resource in resources:
            for time in range(t, t + activity.duration):
                if available_resources[time] < resource[j][k]:
                    impossible = 1
                    break
            if impossible == 1:
                break
        if impossible == 0:
            possible_times.append(t)
    return possible_times


'''
def calculate_resources(active_activities, available_resources):
    n_resources = len(available_resources)
    for activity in active_activities:
        for resource in range(n_resources):
            available_resources[resource]-=activity[2][resource]
    return available_resources
'''


def calculate_eligible_activities(active_activities, available_resources):
    n_resources = len(available_resources)
    unscheduled = [i for i in activities if i not in active_activities and i not in S]
    eligible_activities = []
    for activity in unscheduled:
        impossible = 0
        for resource in range(n_resources):
            if activity[2][resource] > available_resources[resource]:
                impossible = 1
                break
        if impossible == 0:
            eligible_activities.append(activity)
    return eligible_activities



def calculate_eligible_activities(active_activities, available_resources):
    n_resources = resources.number_of()
    unscheduled = [i for i in activities if i not in active_activities and i not in S]
    eligible_activities = []
    for activity in unscheduled:
        impossible = 0
        for resource in range(n_resources):
            if activity[2][resource] > available_resources[resource]:
                impossible = 1
                break
        if impossible == 0:
            eligible_activities.append(activity)
    return eligible_activities
