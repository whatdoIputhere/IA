from tkinter import *
from functions import *
import tkintermapview
from tkinter import filedialog
import tkinter.ttk as ttk

cached_locations = loadCachedLocations()
selectedFile = None
cities = []
city_names = []
algorithms = ['DFS','A*','Greedy Search', 'Uniform Cost']

root = Tk()
root.geometry("1280x720")
left_frame = Frame(root, width=200)
left_frame.pack(side=LEFT, fill=Y,padx=10, pady=10)

def select_map_file():
    global selectedFile
    global city_names 
    global cities
    selectedFile = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Excel files", "*.xlsx"), ("CSV files", "*.csv")])    
    country_name, new_cities = parseTextFile(selectedFile)
    city_names = sorted([city.name for city in new_cities])
    cities = new_cities
    print(city_names)
    map_view.set_position(getGeolocation(country_name,cached_locations)[0], getGeolocation(country_name,cached_locations)[1])
    map_view.set_zoom(7)
    addMarkersToAllLocations(city_names)
    populateCities()

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


def addMarkersToAllLocations(city_names):
    map_view.delete_all_marker()
    for city in city_names:
        location = getGeolocation(city,cached_locations)
        map_view.set_marker(location[0], location[1], city)

select_map_file_button = Button(left_frame, text="Select Map File", command=select_map_file)
select_map_file_button.pack()

start_city_label = Label(left_frame, text="Start City:")
start_city_label.pack()
start_city_combobox = ttk.Combobox(left_frame, values=['Select map first'], width=20, height=20, state="disabled")
start_city_combobox.set(start_city_combobox['values'][0])
start_city_combobox.bind("<<ComboboxSelected>>", populateCities)
start_city_combobox.pack()

end_city_label = Label(left_frame, text="End City:")
end_city_label.pack()
end_city_combobox = ttk.Combobox(left_frame, values=['Select map first'], width=20, height=20, state="disabled")
end_city_combobox.set(end_city_combobox['values'][0])
end_city_combobox.bind("<<ComboboxSelected>>", populateCities)
end_city_combobox.pack()

algorithm_label = Label(left_frame, text="Algorithm:")
algorithm_label.pack()
algorithm_combobox = ttk.Combobox(left_frame, values=algorithms, state="disabled")
algorithm_combobox.set(algorithms[0])
algorithm_combobox.pack()

calculate_route_button = Button(left_frame, text="Calculate Route", command=lambda: handle_calculate_route(cities, start_city_combobox.get(), end_city_combobox.get()))
calculate_route_button.pack()

default_location = getGeolocation("Portugal", cached_locations)

map_view = tkintermapview.TkinterMapView(root, width=1000, height=700)
map_view.set_position(default_location[0], default_location[1])
map_view.set_zoom(0)
map_view.pack(fill=BOTH, expand=True)

root.mainloop()