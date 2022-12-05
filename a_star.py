import math
from heapq import heapify, heappush, heappop

"""
@params:start- tuple of floats used as X Y coord representing the start position
        goal - tuple of floats used as X Y coord representing the end goal position
        field- 2d array of boolean that represents a map for finding optimized path, 0's are navigatable while 1's are impassable
@return:None - No possible path found from start to goal while navigating field
        list[(float, float)] - list of tuples representing the path that can be taken to reach the goal node
"""
def a_star(start: (float,float), goal:(float,float), field: list[list[bool]], h):
    #nodes that are visited but may need to be expanded
    if(not check_bounds(start, field) and not check_bounds(goal, field)):
        return None
    openset = [start]
    heapify(openset)
    
    #For node n, cameFrom[str(n)] is the node immediately preceding it on the cheapest path from start to n currently known
    cameFrom = {} #empty map

    #For node n, gScore[str(n)] is the cost of the cheapest path from start to n currently known.
    gScore = {} #map with default value of Infinity
    gScore[str(start)] = 0 ########### better heuristsic function can be inserted here

    #For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    #how cheap a path could be from start to finish if it goes through n.
    fScore = {} #map with default value of Infinity
    fScore[str(start)] = 0

    while(len(openset)):
        current = heappop(openset) #returns and removes the smallest item on the heap
        if( current == goal):
            #print("current: ",current,"\nREACHED GOAL")
            path = reconstruct_path(cameFrom,current)
            print("Path to goal: ", path)
            return path

        for neighbor in explorable_neighbors(current, field):
            tenative_gScore = gScore[str(current)] + 1
            try:
                gScore[str(neighbor)]
            except(KeyError):
                gScore[str(neighbor)] = math.inf
            if(tenative_gScore < gScore[str(neighbor)]):
                #this path to neighbor is better than any previous one
                cameFrom[str(neighbor)] = current
                gScore[str(neighbor)] = tenative_gScore
                fScore[str(neighbor)] = tenative_gScore + 1 ########### better heuristsic function can be inserted here
                if(neighbor not in openset):
                    heappush(openset, neighbor)

    print("COULD NOT FIND GOAL")
    return None
        

def reconstruct_path(cameFrom: dict, current:(float,float)):
    goal_to_start = [current]
    try:
        while(True):
            back_track = cameFrom[str(current)]
            goal_to_start.append(back_track)
            current = back_track #move backwards
    except(KeyError):
        #current is currently start
        #goal_to_start.append(current)
        #print("reverse path: ",goal_to_start)
        return goal_to_start[-1::-1] #reverse goal to start so it is start to goal


"""
@params: current- tuple of floats used as X Y coords
         field- 2d array of bool telling where terrain is crossable or not
@returns: array of tuples containing X Y coords of explorable neighbors of current
"""
def explorable_neighbors(current: (float, float), field: list[list[bool]]) -> list[(float,float)]:
    neighbors = []

    #check if valid field position
    if(check_bounds((current[0]+1,current[1]),field)): #check row down
        if(not field[current[0]+1][current[1]]):
            neighbors.append((current[0]+1,current[1]))
    if(check_bounds((current[0]-1,current[1]),field)): #check row up
        if(not field[current[0]-1][current[1]]):
            neighbors.append((current[0]-1,current[1]))
    if(check_bounds((current[0],current[1]+1),field)): #check column right
        if(not field[current[0]][current[1]+1]):
            neighbors.append((current[0],current[1]+1))
    if(check_bounds((current[0],current[1]-1),field)): #check column left
        if(not field[current[0]][current[1]-1]):
            neighbors.append((current[0],current[1]-1))
    #print("current: ", current, " Neighbors: ", neighbors)
    return neighbors

"""
@params: current- tuple of floats representing X Y coords
         field- 2d array of which it is checked if current is within the array bounds 
@returns: boolean determining if current is within the bounds of field
"""
def check_bounds(current: (float, float), field: list[list[bool]]) -> bool:
    if(current[0] < 0 or current[1] < 0):
        return False
    try:
        field[current[0]][current[1]]
        return True
    except(IndexError):
        return False


def test():
    def test_hueristic(x):
        return x+1
    field = [ \
        [0,0,0,0,0,0],\
        [0,0,1,0,0,0],\
        [0,1,1,1,0,0],\
        [0,0,0,0,1,0],\
        [0,1,1,0,1,1],\
        [0,1,1,0,0,0]]
    print("check bounds test 1: ",not check_bounds((-6,0),field))
    print("check bounds test 2: ", check_bounds((5,0),field))
    a_star((0,0),(5,5),field,test_hueristic)



if(__name__ == "__main__"):
    test()