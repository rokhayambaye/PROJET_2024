#%%
import osmnx as ox
import networkx as nx
import folium
from folium import Icon
import pandas as pd
from datetime import datetime
from matplotlib import cm
from matplotlib.colors import Normalize

stations_df = pd.read_csv('carte/stations_velomagg.csv')
stations_coords = stations_df[['Latitude', 'Longitude']].values

# TEST
data = {
    "Nom": ["Station A", "Station B", "Station C", "Station D", "Station E"],
    "Latitude": [43.610, 43.611, 43.612, 43.613, 43.614],
    "Longitude": [3.876, 3.877, 3.878, 3.879, 3.880],
    "Intensité": [15, 120, 245, 30, 75]
}
# Créer le DataFrame
compteurs_df = pd.DataFrame(data)

# Intervalles et Poids associés
poids_par_intervalles = [
    ((0, 100), 1), 
    ((100, 200), 2),  
    ((200, 300), 3) 
]

def poids(valeur):
    for (a, b), poids in poids_par_intervalles:
        if a <= valeur < b:
            return poids
    return 0

# Ajout colonne Poids 
compteurs_df['Poids'] = compteurs_df['Intensité'].apply(poids)

# Normaliser les poids
norm = Normalize(vmin=min(p[1] for p in poids_par_intervalles),
                 vmax=max(p[1] for p in poids_par_intervalles))

G = ox.graph_from_place( "Montpellier, France", network_type='bike')

# Noeuds les plus proches
stations_nodes = []
for id, row in stations_df.iterrows():
    lat, lon = row['Latitude'], row['Longitude']
    node = ox.distance.nearest_nodes(G, X=lon, Y=lat)
    stations_nodes.append((node, row['Nom']))

# Extraire tous les chemins entre les stations (par pairs)
paths = []
for i in range(len(stations_nodes) - 1):
    start_node = stations_nodes[i][0]
    end_node = stations_nodes[i + 1][0]
    if nx.has_path(G, start_node, end_node):
        try:
            route = nx.shortest_path(G, start_node, end_node, weight='length')
            paths.append(route)
        except nx.NetworkXNoPath:
            print(f"No valid path between {stations_nodes[i][1]} and {stations_nodes[i + 1][1]}")
    else:
        print(f"No path found between {start_node} and {end_node}")

# Obtenir le contour de la ville de Montpellier
area = ox.geocode_to_gdf("Montpellier, France")

fds_coord = [43.6312537,3.8612405] # Coordonnées de la Faculté des Sciences de Montpellier

days_of_week = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# Créer une carte pour chaque jour de la semaine
for day in days_of_week:
    m = folium.Map(location=[43.6117, 3.8777], zoom_start=13)
    m.get_root().html.add_child(folium.Element(f"<h3 style='position: fixed; top: 10px; left: 10px; background-color: white; padding: 5px;'>Carte du {day}</h3>"))

    # Faculté des Sciences
    folium.Marker(
        location=fds_coord,
        popup="Faculté des Sciences",
        icon=Icon(icon="university", color="RED", prefix="fa")
    ).add_to(m)

    # Contour de la ville
    folium.GeoJson(
        data=area["geometry"],
        style_function=lambda x: {
            "color": "black",
            "weight": 2,
            "fillOpacity": 0
        }
    ).add_to(m)

    # Stations Velomagg
    for id, row in stations_df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=row['Nom'],
            icon=Icon(icon='bicycle', color='black', prefix='fa', icon_size=(15, 15))
        ).add_to(m)

    # Ecocompteurs
    for id, row in compteurs_df.iterrows():
        color = cm.viridis(norm(row['Poids']))
        hex_color = f"#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}"
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=8 + row['Poids'],
            color=hex_color,
            fill=True,
            fill_color=hex_color,
            fill_opacity=0.7,
            popup=f"{row['Nom']}<br>Poids: {row['Poids']}<br>Intensité: {row['Intensité']}"
        ).add_to(m)
        
    # Chemins
    for route in paths:
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        folium.PolyLine(locations=route_coords, color='blue', weight=4, opacity=0.7).add_to(m)

    m.save(f"carte/map_montpellier_{day}.html")