from functions import *


def uniform_cost_algorithm(cities, start_city, end_city, heuristic_value=0):
    stop = False
    paths = []
    path_cost = []  # path cost without heuristic
    path_cost_total = []  # includes heuristic
    lowest_cost_path = {}
    latest_lowest_cost_path = {}
    is_first_iteration = True

    while not stop:
        for connection in start_city.getConnections():
            city = [city for city in cities if city.getName() ==
                    connection["name"]][0]

            if city.getName() == end_city.getName():
                print("end")
                return [], []

            aux_path = []
            aux_cost = 0
            if paths == [] or is_first_iteration:
                aux_path.append(start_city.getName())
                aux_path.append(city.getName())
                aux_cost = int(connection["distance"]) + int(heuristic_value)
            else:
                for path in paths:
                    aux_path = path["path"].copy()
                    aux_cost = path["cost"]
                aux_path.append(city.getName())
                aux_cost += int(connection["distance"]) + int(heuristic_value)

            paths.append({"path": aux_path, "cost": aux_cost})

        if is_first_iteration:
            is_first_iteration = False

        print(paths)
        for path in paths:
            if lowest_cost_path == {} or path["cost"] < lowest_cost_path["cost"]:
                lowest_cost_path = path

        print(lowest_cost_path["path"][-1])
        if lowest_cost_path != latest_lowest_cost_path or latest_lowest_cost_path == {}:
            latest_lowest_cost_path = lowest_cost_path

            paths.remove(lowest_cost_path)

            next_city = [city for city in cities if city.getName()
                         == lowest_cost_path["path"][-1]][0]

            start_city = next_city

    return [], []


def uniform_cost(cities, start_city, end_city):
    return uniform_cost_algorithm(cities, start_city, end_city)


def depth_limited_search(cities, start_city, end_city, depth_limit, current_depth=0, path=[], path_cost=[]):
    if current_depth == depth_limit:
        print("Limite de profundidade excedido")
        return [], []

    path.append(start_city.getName())
    path_cost.append(0)

    for connection in start_city.getConnections():
        city = next((city for city in cities if city.getName()
                    == connection["name"]), None)
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
            new_path, new_distance = depth_limited_search(
                cities, city, end_city, depth_limit, current_depth + 1, path, path_cost)
            if new_path is not None:
                return new_path, new_distance

    return [], []


def greedy_search(cities, start_city, end_city, greedypath=[], greedycost=[]):
    minHeuristic = 99999
    nextcity = None
    nextcitydistance = 0

    greedypath.append(start_city.getName())
    for connection in start_city.getConnections():
        city = [city for city in cities if city.getName() ==
                connection["name"]][0]
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
    return uniform_cost_algorithm(cities, start_city, end_city, heuristic_value=start_city.getStraightDistanceToFaro())
