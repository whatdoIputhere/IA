import os
import inquirer
import pandas as pd
folder_path = "maps"
algorithms = ["lp", "cu", "pp", "pl", "ap","ps","a*"]
def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def parseTextFile(file):
    filepath = folder_path+'\\'+file

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        graph = {}
        for line in lines:
            city, *connections = line.split(',')
            if(city not in graph):
                graph[city] = []
            for connection in connections:
                connection_city = connection.split('(')[0].strip()
                connection_distance = connection.split('(')[1].split(')')[0].strip()
                graph[city].append({connection_city: connection_distance})
                if connection_city not in graph:
                    graph[connection_city] = [{city: connection_distance}]
                else:
                    graph[connection_city].append({city: connection_distance})
            
    input("Press Enter to continue...")
    return graph
    
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
        graph = parseTextFile(selectedfile)
             
    return {"filename": selectedfile, "data": graph}

def lp(data, start, end):
    path = [start]
    for city in data:
        if city == start:
            for connection in data[city]:
                print(connection)
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
    
def printMapData(data):
    clearScreen()
    for city, connections in data.items():
        print(f"{city}: {connections}")
    input("\nPress Enter to return...")