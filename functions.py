import os
import inquirer
import pandas as pd
from geopy.geocoders import Photon
from city import City
folder_path = "maps"
algorithms = ["lp", "cu", "pp", "pl", "ap","ps","a*"]

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def parseTextFile(file,cached_locations):
    cities = []
    countryname = ""
    
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        for line in lines:
            if line == lines[0]:
                countryname = line.strip()
                continue
            
            cityName, *connections = line.split(',')
            if(not any(cityName == city.getName() for city in cities)):
                cityLocation = getGeolocation(cityName, cached_locations, countryname)
                city = City(cityName, cityLocation)
                cities.append(city)
            else:
                for index, c in enumerate(cities):
                    if c.getName() == cityName:
                        city = cities[index]
            
            for connection in connections:
                connection_city = connection.split('(')[0].strip()
                connection_distance = connection.split('(')[1].split(')')[0].strip()
                city.addConnection({"name": connection_city, "distance": connection_distance})
                if not any(connection_city == city.getName() for city in cities):
                    connection_city_location = getGeolocation(connection_city, cached_locations, countryname)
                    connectionCity = City(connection_city,connection_city_location)
                    connectionCity.addConnection({"name": cityName, "distance": connection_distance})
                    cities.append(connectionCity)
                else:
                    for index, c in enumerate(cities):
                        if c.getName() == connection_city:                        
                            cities[index].addConnection({"name": cityName, "distance": connection_distance})
        
    print(f"Number of cities: {len(cities)}")
    for city in cities:
        city.printConnections()
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
    
    
def loadCachedLocations():
    #print("Loading cached locations...")
    cached_locations = []
    open("cached_locations.txt", "a").close()
    with open("cached_locations.txt", "r", encoding="utf-8") as file:
        for line in file:
            location, latitude, longitude = line.split(',')
            cached_locations.append({"location": location, "latitude": float(latitude), "longitude": float(longitude)})
    return cached_locations

def getGeolocation(location, cached_locations, country=""):
    if location in [loc["location"] for loc in cached_locations]:
        print(f"Using cached location for {location}.")
        cached_location = next((loc for loc in cached_locations if loc["location"] == location), None)
        return [cached_location["latitude"], cached_location["longitude"]]
    print(f"Geolocating {location}...")
    geolocator = Photon(user_agent="ia202324")
    geolocation = geolocator.geocode(location + ", " + country if country != "" else location)
    cached_locations.append({"location": location, "latitude": geolocation.latitude, "longitude": geolocation.longitude})
    with open("cached_locations.txt", "a", encoding="utf-8") as file:
        file.write(f"{location},{geolocation.latitude},{geolocation.longitude}\n")
    return [geolocation.latitude, geolocation.longitude]