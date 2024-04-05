from functions import * 

def uniform_cost(cities, start_city, end_city):
    print("Uniform Cost Search")
    
def depth_limited_search(cities, start_city, end_city, depth_limit, current_depth=0, path=[], distance=0):
    if current_depth == depth_limit:
        print("Depth Limit Exceeded")
        return None, None

    path.append(start_city.getName())

    for connection in start_city.getConnections():
        city = next((city for city in cities if city.getName() == connection["name"]), None)
        if city is None:
            continue
        if city.getName() == end_city.getName():
            distance += int(connection["distance"])  # Make sure distance is an integer
            print("Path found:", path + [end_city.getName()])
            print("Distance:", distance)
            return path + [end_city.getName()], distance
        else:
            new_path, new_distance = depth_limited_search(cities, city, end_city, depth_limit, current_depth + 1,
                                                          path.copy(), distance + int(connection["distance"]))
            if new_path is not None:
                return new_path, new_distance

    return None, None

def greedy_search(cities, start_city, end_city, greedypath = [], greedycost = []):
    minHeuristic = 99999;
    nextcity = None
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
    greedycost.append(connection["distance"])
    try:
        return greedy_search(cities, nextcity, end_city, greedypath, greedycost)
    except Exception as e:
        return [], []

def a_star(cities, start_city, end_city):
    print("A* Search")
