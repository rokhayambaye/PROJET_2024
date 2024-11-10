import osmnx as ox
import networkx as nx
import folium
from folium import Icon
import pandas as pd


stations_df = pd.read_csv('carte/stations_velomagg.csv')
stations_coords = stations_df[['Latitude', 'Longitude']].values

G = ox.graph_from_place( "Montpellier, France", network_type='bike')

# Trouver les nœuds les plus proches des stations
stations_nodes = []
for id, row in stations_df.iterrows():
    lat, lon = row['Latitude'], row['Longitude']
    node = ox.distance.nearest_nodes(G, X=lon, Y=lat)
    if node not in G:
        print(f"Le nœud pour la station {row['Nom']} n'est pas dans le réseau cyclable.")
    else:
        stations_nodes.append((node, row['Nom']))  # Ajouter le nom de la station ici

# Extraire tous les chemins entre les stations (par pairs)
paths = []
for i in range(len(stations_nodes) - 1):
    start_node = stations_nodes[i][0]
    end_node = stations_nodes[i + 1][0]
    
   # Tester s'il y a un chemin entre les stations
    if nx.has_path(G, start_node, end_node):
        try:
            route = nx.shortest_path(G, start_node, end_node, weight='length')
            paths.append(route)
        except nx.NetworkXNoPath:
            print(f"No valid path between {stations_nodes[i][1]} and {stations_nodes[i + 1][1]}")
    else:
        print(f"No path found between {start_node} and {end_node}")

# Créer une carte centrée sur Montpellier
m = folium.Map(location=[43.6117, 3.8777], zoom_start=13)

# Ajouter les stations à la carte avec leurs noms
for id, row in stations_df.iterrows():
    lat, lon = row['Latitude'], row['Longitude']
    station_name = row['Nom']
    folium.Marker(location=[lat, lon], popup=station_name,icon=Icon(icon='bicycle', color='black', prefix='fa', icon_size=(20, 20))).add_to(m)

# Tracer les chemins passant par les stations
for route in paths:
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
    folium.PolyLine(locations=route_coords, color='red', weight=4, opacity=0.7).add_to(m)

m.save("carte/map_montpellier.html")