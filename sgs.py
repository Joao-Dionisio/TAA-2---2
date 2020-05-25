# We need to check what the input is

def read_file(file):

    # This is so much data wtf
    # For now, let's deliver the data like
    #[..., [activity i, duration, [resources], [sucecessors]], ....]
    # So, for jobnr. 1 of j30 of the first dataset we have
    # [[1, 0, [0,0,0,0], [2,3,4]], [2, 2, [1,2,4,0], [10,11,28]], ... ]
    return activities

# We then feed read_file into sgs

def sgs(activities):
    successors = [i[3] for i in activities]
    resource = [i[2] for i in activities]
    duration = [i[1] for i in activities]
    activities = [i for i in range(activities[-1])]
    precedents = calculate_precedents(successors)
    S = [0] # First dummy activity
    l = activities[-1]
    F = l*[0]
    LF = calculate_latest_finish(activities)
    for i in range(l):
        D, F, R = calculate_variables(activities)
        cur_activity = activities[D[0]]
        precedent_finish_times = [F[activities[j]] for j in precedents[j]]
        EF = max(precedent_finish_times) + duration[j]
        possible_times = calculate_possible_times(activities[i])
        F[j] = min(possible_times) + p[j]
        S.append(j)
        if i < l-1:
            D = D[1:] # I think that if it doesn't pass this then it's impossible
            D.extend()
                
    F[-1] = max(F) # The last activity will be a precedent of activity n
    return F[-1]


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

    
def calculate_variables(activities):

    return D, F, R

                
def calculate_latest_finish(activities):
    
    return

                
def calculate_possible_times(activity):
    initial_times = [i for i in F[:j] if i >= EF[j] - duration[j] and i <= LF[j] - duration[j]]
    possible_times = []
    for t in initial_times:
        resource_available = 0
        for resource in resources:
            for time in range(t, t+duration[j]):
                if available_resources[time] < resource[j][k]:
                    resource_available = 1
                    break
            if resource_available == 1:
                break
        if resource_available == 0:
            possible_times.append(t)
    return possible_times
