from functions import * 

def uniform_cost(cities, start_city, end_city):
    print("Uniform Cost Search")
    # print(cities) 
    print(start_city.getName())
    print(end_city.getConnections())  
    print(end_city.getName())  
    # Priority queue
    queue = [(0, start_city)]
    
    # To keep track of visited cities
    visited = set()
    current_city = start_city.getName()

    while queue:
        # Sort the queue then pop the item with smallest cost
        queue.sort(reverse=True)
        cost, current_city = queue.pop()
        
       
        if current_city == end_city:
            print("Path found with total cost:",cost)
            return
        
        if current_city not in visited:
            visited.add(current_city)
            min_distance = int(99999)
            name_connection = None


            for connection in start_city.getConnections():
                print("conecctions: ", connection)
                if int(connection["distance"]) < min_distance:
                    min_distance = int(connection["distance"])
                    current_city = connection["name"]
                    print('current_city :', current_city)
                    queue.append((min_distance, connection["name"]))    
            visited.add(current_city)       

    print("Path not found")
    return
    

    
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
            distance += int(connection["distance"])
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
