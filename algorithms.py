from functions import * 

def uniform_cost(cities, start_city, end_city):
    print("Uniform Cost Search")
    
def depth_limited_search(cities, start_city, end_city):
    print("Depth Limited Search")

def greedy_search(cities, start_city, end_city, greedypath = [], greedycost = []):
    minHeuristic = 99999;
    nextcity = None
    greedypath.append(start_city.getName())
    for connection in start_city.getConnections():
        city = [city for city in cities if city.getName() == connection["name"]][0]
        if city.getName() == end_city.getName():
            greedypath.append(city.getName())
            greedycost.append(connection["distance"])
            return greedypath, greedycost
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