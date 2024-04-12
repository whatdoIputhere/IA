from functions import * 

def uniform_cost_algorithm(cities, start_city, end_city, path = [], cost = [], heuristic_value = 0):
    min_distance = 99999
    next_city = None
    
    path.append(start_city.getName())
    for connection in start_city.getConnections():
        city = [city for city in cities if city.getName() == connection["name"]][0]
        if city.getName() == end_city.getName():
            path.append(city.getName())
            cost.append(connection["distance"])
            result = (path.copy(), cost.copy()) 
            cost.clear()
            path.clear()
            return result
        
        if int(connection["distance"]) < min_distance:
            min_distance = int(connection["distance"]) + int(heuristic_value)
            next_city = city

    cost.append(min_distance)
            
    try:
        return uniform_cost_algorithm(cities, next_city, end_city, path, cost)
    except Exception as e:
        print(e)
        return [], []
    
    
def uniform_cost(cities, start_city, end_city):
    print("Uniform Cost Search")
    
    return uniform_cost_algorithm(cities, start_city, end_city)
    
    
def depth_limited_search(cities, start_city, end_city, depth_limit, current_depth=0, path=[], path_cost=[]):
    if current_depth == depth_limit:
        print("Limite de profundidade excedido")
        return [], []

    path.append(start_city.getName())
    path_cost.append(0)

    for connection in start_city.getConnections():
        city = next((city for city in cities if city.getName() == connection["name"]), None)
        if city is None:
            continue
        if city.getName() == end_city.getName():
           
            path.append(city.getName())
            path_cost.append(connection["distance"])
            result = (path.copy(), path_cost.copy()) 
            path_cost.clear()
            path.clear()
            return result
            
        else:
            new_path, new_distance = depth_limited_search(cities, city, end_city, depth_limit, current_depth + 1,path, path_cost)
            if new_path is not None:
                return new_path, new_distance

    return [], []

def greedy_search(cities, start_city, end_city, greedypath = [], greedycost = []):
    minHeuristic = 99999
    nextcity = None
    nextcitydistance = 0
    
    greedypath.append(start_city.getName())    
    for connection in start_city.getConnections():
        city = [city for city in cities if city.getName() == connection["name"]][0]
        if city.getName() == end_city.getName():
            greedypath.append(city.getName())
            greedycost.append(connection["distance"])
            result = (greedypath.copy(), greedycost.copy()) 
            greedycost.clear()
            greedypath.clear()
            return result
        
        if int(city.getStraightDistanceToFaro()) < int(minHeuristic):
            minHeuristic = city.getStraightDistanceToFaro()
            nextcity = city
            nextcitydistance = connection["distance"]
            
    greedycost.append(nextcitydistance)
    
    try:
        return greedy_search(cities, nextcity, end_city, greedypath, greedycost)
    except Exception as e:
        return [], []

def a_star(cities, start_city, end_city):
    return uniform_cost_algorithm(cities, start_city, end_city, heuristic_value = start_city.getStraightDistanceToFaro())
