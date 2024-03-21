import inquirer
import functions
#pip install pandas, inquirer, openpyxl
selectedMap = {"filename": None, "data": None}
while True:
    functions.clearScreen()
    options = [
        inquirer.List('action',
                    message="Select an action",
                    choices=[
                            ('Select map file', 1), 
                            ('Exit',0)] 
                    if selectedMap['filename'] is None 
                    else [
                        (f"Select map file (Currently selected: {selectedMap['filename']})",1), 
                        ("Calculate route",2), 
                        ("Print map data",3), 
                        ("Exit",0)
                        ]
                    )
    ]
    selectedoption = inquirer.prompt(options)
    action = selectedoption['action']
    # TODO: Add menu options to select start and end cities and algorithm
    match action:
        case 1:
            selectedMap = functions.handle_select_map_file()
        case 2:
            functions.handle_calculate_route(selectedMap['data'], "Aveiro", "Faro", "dfs")
        case 3:
            functions.printMapData(selectedMap['data'])
        case 0:
            break