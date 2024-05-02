from functions import *


def get_city_object(cities, city_name):
    return [city for city in cities if city.getName() == city_name][0]


def uniform_cost_algorithm(cities, start_city, end_city, isFromAStar=False):
    paths = []
    lowest_cost_path = {}
    latest_lowest_cost_path = {}
    is_first_iteration = True

    while True:
        for connection in start_city.getConnections():
            city = get_city_object(cities, connection["name"])

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
                h(city, end_city) if isFromAStar else 0)

            paths.append({"paths": aux_paths, "costs": aux_costs,
                         "total_cost": aux_total_cost})

            if city.getName() == end_city.getName():
                result = (paths[-1]["paths"].copy(), paths[-1]["costs"].copy())
                paths.clear()
                return result

        if is_first_iteration:
            is_first_iteration = False

        lowest_cost_path = min(paths, key=lambda path: path["total_cost"])
        if lowest_cost_path != latest_lowest_cost_path or latest_lowest_cost_path == {}:
            latest_lowest_cost_path = lowest_cost_path

            next_city = get_city_object(cities, lowest_cost_path["paths"][-1])
            paths.remove(lowest_cost_path)

            start_city = next_city


def uniform_cost(cities, start_city, end_city):
    return uniform_cost_algorithm(cities, start_city, end_city)


def depth_limited_search(cities, start_city, end_city, depth_limit):
    path = []
    path_cost = []
    current_depth = 0
    start_city_connections = []
    start_city_connections = start_city.getConnections().copy()

    path.append(start_city.getName())
    while True:
        for connection in start_city.getConnections():
            city = get_city_object(cities, connection["name"])

            if city.getName() == end_city.getName():
                path.append(city.getName())
                path_cost.append(int(connection["distance"]))
                result = (path.copy(), path_cost.copy())
                path.clear()
                path_cost.clear()
                return result

            if current_depth == depth_limit:
                if start_city_connections != []:
                    start_city_connections.pop(0)
                    current_depth = 0
                    #! FIX: PATH VERDADEIRO ATÉ AO DESTINO
                    aux = path[0]
                    path = []
                    path_cost = []
                    path.append(aux)

                    if start_city_connections != []:
                        next_city = get_city_object(
                            cities, start_city_connections[0]["name"])
                        start_city = next_city
                        path.append(start_city.getName())
                    else:
                        print("Limite de profundidade excedido")
                        return [], []
                else:
                    print("Limite de profundidade excedido")
                    return [], []
            else:
                current_depth += 1
                path.append(city.getName())
                path_cost.append(int(connection["distance"]))

                start_city = city


def greedy_search(cities, start_city, end_city, greedypath=[], greedycost=[]):
    minHeuristic = 99999
    nextcity = None
    nextcitydistance = 0

    greedypath.append(start_city.getName())
    for connection in start_city.getConnections():
        city = get_city_object(cities, connection["name"])

        if city.getName() == end_city.getName():
            greedypath.append(city.getName())
            greedycost.append(connection["distance"])
            result = (greedypath.copy(), greedycost.copy())
            greedypath.clear()
            greedycost.clear()
            return result

        if h(city, end_city) < minHeuristic:
            minHeuristic = h(city, end_city)
            nextcity = city
            nextcitydistance = connection["distance"]

    greedycost.append(nextcitydistance)

    try:
        return greedy_search(cities, nextcity, end_city, greedypath, greedycost)
    except Exception as e:
        return [], []


def a_star(cities, start_city, end_city):
    return uniform_cost_algorithm(cities, start_city, end_city, isFromAStar=True)
