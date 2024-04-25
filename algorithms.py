from functions import *


def uniform_cost_algorithm(cities, start_city, end_city, isFromAStar=False):
    stop = False
    paths = []
    lowest_cost_path = {}
    latest_lowest_cost_path = {}
    is_first_iteration = True

    while not stop:
        for connection in start_city.getConnections():
            city = [city for city in cities if city.getName() ==
                    connection["name"]][0]

            aux_paths = []
            aux_costs = []
            aux_total_cost = 0
            if paths == [] or is_first_iteration:
                aux_paths.append(start_city.getName())
            else:
                aux_paths = lowest_cost_path["paths"].copy()
                aux_costs = lowest_cost_path["costs"].copy()
                aux_total_cost = lowest_cost_path["total_cost"]
            aux_paths.append(city.getName())
            aux_costs.append(int(connection["distance"]))
            aux_total_cost += int(connection["distance"]) + (
                int(city.getStraightDistanceToFaro()) if isFromAStar else 0)

            paths.append({"paths": aux_paths, "costs": aux_costs,
                         "total_cost": aux_total_cost})

            if city.getName() == end_city.getName():
                return (paths[-1]["paths"].copy(), paths[-1]["costs"].copy())

        if is_first_iteration:
            is_first_iteration = False

        lowest_cost_path = min(paths, key=lambda path: path["total_cost"])
        if lowest_cost_path != latest_lowest_cost_path or latest_lowest_cost_path == {}:
            latest_lowest_cost_path = lowest_cost_path

            next_city = [city for city in cities if city.getName()
                         == lowest_cost_path["paths"][-1]][0]
            paths.remove(lowest_cost_path)

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
    return uniform_cost_algorithm(cities, start_city, end_city, isFromAStar=True)
