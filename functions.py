import os
import inquirer
import pandas as pd
folder_path = "maps"

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def parseTextFile(file):
    filepath = folder_path+'\\'+file

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        graph = {}
        for line in lines:
            city, *connections = line.split(',')
            graph[city] = [connection.strip() for connection in connections]
    return graph
    print()
    input("Press Enter to continue...")
    
def parseExcelFile(file):
    filepath = folder_path+'\\'+file
    
    data = pd.read_excel(filepath,header=None)
    graph = {}
    for index, row in data.iterrows():
        city, *connections = row.values
        graph[city] = [connection for connection in connections if pd.notna(connection)]
        
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
             
    return {"file": selectedfile, "data": graph}
    
def handle_calculate_route():
    print('Calculating route')

def printMapData(data):
    clearScreen()
    print(data)
    input("\nPress Enter to return...")