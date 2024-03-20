#pip install networkx, matplotlib

# region Graph example
import networkx as nx
import matplotlib.pyplot as plt
def parse_csv(file_path):
    G = nx.Graph()
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            city, *connections = row      
            for connection in connections:
                connected_city, distance = connection.split('-')
                G.add_edge(city, connected_city.strip(), weight=int(distance))
    return G

def draw_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

# G = parse_csv('./maps/map.csv')
# draw_graph(G)
# # endregion