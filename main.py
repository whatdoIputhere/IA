import inquirer
import functions
#pip install pandas, inquirer, openpyxl
selectedMap = {"file": None, "data": None}
while True:
    functions.clearScreen()
    calculateRouteText = 'Calculate route (no map file selected)' if selectedMap['file'] is None else f"Calculate route ({selectedMap['file']})"
    options = [
        inquirer.List('action',
                    message="Select an action",
                    choices=['Select map file', 'Exit'] if selectedMap['file'] is None 
                    else [f"Select map file (Currently selected: {selectedMap['file']})", "Calculate route", 'Print map data', 'Exit'])
    ]    
    
    selectedoption = inquirer.prompt(options)
    action = selectedoption['action']
    
    if 'Select map file' in action:
        selectedMap = functions.handle_select_map_file()
    elif action == 'Calculate route':
        functions.handle_calculate_route(selectedMap['data'])
    elif action == 'Print map data':
        functions.printMapData(selectedMap['data'])
    elif action == 'Exit':
        break