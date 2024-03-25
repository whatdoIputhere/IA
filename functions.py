import os
import inquirer
import pandas as pd
from geopy.geocoders import Photon
from city import City
folder_path = "maps"
algorithms = ["lp", "cu", "pp", "pl", "ap","ps","a*"]

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def parseTextFile(file):
    filepath = file
    cities = []
    countryname = ""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        graph = {}
        
        for line in lines:
            if line == lines[0]:
                countryname = line.strip()
                continue
            
            cityName, *connections = line.split(',')
            
            if not any(cityName == city.name for city in cities):
                city = City(cityName)
                cities.append(city)
            
            for connection in connections:
                connection_city = connection.split('(')[0].strip()
                connection_distance = connection.split('(')[1].split(')')[0].strip()
                city.addConnection({"name": connection_city, "distance": connection_distance})
                if not any(connection_city == city.name for city in cities):
                    connectionCity = City(connection_city)
                    connectionCity.addConnection({"name": cityName, "distance": connection_distance})
                    cities.append(connectionCity)
                else:
                    for c in cities:
                        if c.name == connection_city:
                            c.addConnection({"name": cityName, "distance": connection_distance})                        
            
    # input("Press Enter to continue...")
    return countryname, cities
    
def parseExcelFile(file):
    filepath = folder_path+'\\'+file
    
    data = pd.read_excel(filepath,header=None)
    graph = {}
    for index, row in data.iterrows():
        city, *connections = row.values
        if city not in graph:
            graph[city] = []
        for connection in connections:
            if pd.notna(connection):
                connection_city = connection.split('(')[0].strip()
                connection_distance = connection.split('(')[1].split(')')[0].strip()
                graph[city].append({connection_city: connection_distance})
                if connection_city not in graph:
                    graph[connection_city] = [{city: connection_distance}]
                else:
                    graph[connection_city].append({city: connection_distance})
        
    return graph

def handle_select_map_file():
    files = [f for f in os.listdir(folder_path) if f.endswith(('.xlsx', '.txt', '.csv'))]
    fileoptions = [
        inquirer.List('mapfile',
                      message="Select a map file",
                      choices=files,)
    ]
    selectedfile = inquirer.prompt(fileoptions)['mapfile']
        
    if selectedfile.endswith('.xlsx'):
        graph = parseExcelFile(selectedfile)
    elif selectedfile.endswith('.txt') or selectedfile.endswith('.csv'):
        cities = parseTextFile(selectedfile)
             
    return {"filename": selectedfile, "cities": cities}

def lp(data, start, end):
    path = [start]
    for city in data:
        if city == start:
            for connection in data[city]:
                pass
    input()
    return path

def handle_calculate_route(data):
    clearScreen()
    cityoptions = [
        inquirer.List('city',
                      message="Select start city",
                      choices=data.keys(),)
    ]
    selectedStartcity = inquirer.prompt(cityoptions)['city']
    clearScreen()
    print(f"Selected start city: {selectedStartcity}")
    cityoptions = [
        inquirer.List('city',
                      message="Select end city",
                      choices=[city for city in data.keys() if city != selectedStartcity],)
    ]
    selectedEndcity = inquirer.prompt(cityoptions)['city']
    
    algorithmoptions = [
        inquirer.List('algorithm',
                      message="Select algorithm",
                      choices=algorithms,)
    ]
    clearScreen()
    print(f"Selected start city: {selectedStartcity}")
    print(f"Selected end city: {selectedEndcity}")
    selectedalgorithm = inquirer.prompt(algorithmoptions)['algorithm']
    
    if selectedalgorithm == "lp":
        path = lp(data, selectedStartcity, selectedStartcity)
    print(path)
    input("\nPress Enter to return...")
    
def printMapData(cities):
    clearScreen()
    for city in cities:
        print(city.__str__())
    input("\nPress Enter to return...")
    
    
def loadCachedLocations():
    print("Loading cached locations...")
    cached_locations = []
    open("cached_locations.txt", "a").close()
    with open("cached_locations.txt", "r", encoding="utf-8") as file:
        for line in file:
            location, latitude, longitude = line.split(',')
            cached_locations.append({"location": location, "latitude": float(latitude), "longitude": float(longitude)})
    return cached_locations

def getGeolocation(location, cached_locations):
    if location in [loc["location"] for loc in cached_locations]:
        print(f"Using cached location for {location}.")
        cached_location = next((loc for loc in cached_locations if loc["location"] == location), None)
        return [cached_location["latitude"], cached_location["longitude"]]
    print(f"Geolocating {location}...")
    geolocator = Photon(user_agent="ia202324")
    geolocation = geolocator.geocode(location)
    cached_locations.append({"location": location, "latitude": geolocation.latitude, "longitude": geolocation.longitude})
    with open("cached_locations.txt", "a", encoding="utf-8") as file:
        file.write(f"{location},{geolocation.latitude},{geolocation.longitude}\n")
    return [geolocation.latitude, geolocation.longitude]