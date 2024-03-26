from tkinter import *
from functions import *
import tkintermapview
from tkinter import filedialog
import tkinter.ttk as ttk

cached_locations = loadCachedLocations()
selectedFile = None
cities = ()
city_names = ()
algorithms = ['DFS','A*','Greedy Search', 'Uniform Cost']
default_location = getGeolocation("Portugal", cached_locations)


install_requirements()
root = Tk()
root.geometry("1280x720")
root.title("Projeto IA")
root.configure(background='#DDD')
left_frame = Frame(root, width=200)
left_frame.pack(side=LEFT, fill=Y, ipadx=15)

def select_map_file():
    global selectedFile
    global city_names 
    global cities
    global map_view
    try:
        selectedFile = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Excel files", "*.xlsx"), ("CSV files", "*.csv")])        
        if selectedFile.endswith('.xlsx'):
            country_name, new_cities = parseExcelFile(selectedFile, cached_locations)
        else:
            country_name, new_cities = parseTextFile(selectedFile, cached_locations)
        city_names = sorted([city.name for city in new_cities])
        cities = new_cities
        countryLocation = getGeolocation(country_name, cached_locations)        
        
        try:
            map_view.set_position(countryLocation[0], countryLocation[1])
        except:
            map_view = loadMap()

        clearMarkersAndPaths()
        populateCities()
        print(f"Number of cities: {len(cities)}")
        for city in cities:
            city.printConnections()
    except Exception as e:
        print("Error:", str(e))

def populateCities(event=None):
    if event is None:
        start_city_combobox['values'] = [city_names[0]] + city_names[2:]
        end_city_combobox['values'] = city_names[1:]
        start_city_combobox.set(city_names[0])
        end_city_combobox.set(city_names[1])
        start_city_combobox.state(["!disabled"])
        end_city_combobox.state(["!disabled"])
        algorithm_combobox.state(["!disabled"])
    else:
        widget = event.widget

        if widget == start_city_combobox:
            end_city_combobox['values'] = [city for city in city_names if city != start_city_combobox.get()]
        elif widget == end_city_combobox:
            start_city_combobox['values'] = [city for city in city_names if city != end_city_combobox.get()]

def clearMarkersAndPaths():
    map_view.delete_all_marker()
    map_view.delete_all_path()

def addMarkersToAllLocations():
    map_view.delete_all_marker()
    for city in city_names:
        location = getGeolocation(city,cached_locations)
        map_view.set_marker(location[0], location[1], city)

def addPathsToMap():
    map_view.delete_all_path()
    addMarkersToAllLocations()
    for city in cities:
        for connection_city in city.getConnections():
            connection = [c for c in cities if c.getName() == connection_city['name']][0]
            path = [(city.latitude, city.longitude), (connection.latitude, connection.longitude)]
            map_view.set_path(path)
            
select_map_file_button = Button(left_frame, text="Select Map File", command=select_map_file)
select_map_file_button.pack(pady=(20,0))

start_city_label = Label(left_frame, text="Start City:")
start_city_label.pack(pady=(10,0))
start_city_combobox = ttk.Combobox(left_frame, values=['Select map first'], width=20, height=20, state="disabled")
start_city_combobox.set(start_city_combobox['values'][0])
start_city_combobox.bind("<<ComboboxSelected>>", populateCities)
start_city_combobox.pack()

end_city_label = Label(left_frame, text="End City:")
end_city_label.pack(pady=(10,0))
end_city_combobox = ttk.Combobox(left_frame, values=['Select map first'], width=20, height=20, state="disabled")
end_city_combobox.set(end_city_combobox['values'][0])
end_city_combobox.bind("<<ComboboxSelected>>", populateCities)
end_city_combobox.pack()

algorithm_label = Label(left_frame, text="Algorithm:")
algorithm_label.pack(pady=(10,0))
algorithm_combobox = ttk.Combobox(left_frame, values=algorithms, state="disabled")
algorithm_combobox.set(algorithms[0])
algorithm_combobox.pack()

calculate_route_button = Button(left_frame, text="Calculate Route", 
                                command=lambda: handle_calculate_route(cities, start_city_combobox.get(), end_city_combobox.get()))
calculate_route_button.pack(pady=(10,0))

add_markers_and_distances_button = Button(left_frame, text="Add Markers and Distances", command=lambda: addPathsToMap())
add_markers_and_distances_button.pack()

select_map_message = Label(text="Select a file to load the map.", font=("Arial", 16),foreground="#666",background="#DDD")
select_map_message.pack()
select_map_message.place_configure(relx=0.5, rely=0.5, anchor=CENTER)


def loadMap():
    select_map_message.pack_forget()
    map_view = tkintermapview.TkinterMapView(root, width=1000, height=700)
    map_view.set_position(default_location[0], default_location[1])
    map_view.set_zoom(7)
    map_view.pack(fill=BOTH, expand=True)
    return map_view

root.mainloop()