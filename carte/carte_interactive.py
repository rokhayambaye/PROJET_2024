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

# Créer le DataFrame
compteurs_df = pd.read_csv('Base_des_donnes/donnees_montpellier_2023.csv', delimiter=';')
compteurs_df = compteurs_df[['intensity','date','longitude','latitude']]

# Intervalles et Poids associés par tranche de 600
poids_par_intervalles = [
    ((0, 600), 1), 
    ((600, 1200), 2),  
    ((1200, 1800), 3),
    ((1800, 2400), 4),
    ((2400, 3700), 5),
]

def poids(valeur):
    for (a, b), poids in poids_par_intervalles:
        if a <= valeur < b:
            return poids
    return 0

# Ajout colonne Poids 
compteurs_df['weight'] = compteurs_df['intensity'].apply(poids)

# Normaliser les poids
norm = Normalize(vmin=min(p[1] for p in poids_par_intervalles),
                 vmax=max(p[1] for p in poids_par_intervalles))

G = ox.graph_from_place( "Montpellier, France", network_type='all')

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

# Contour de la ville
area = ox.geocode_to_gdf("Montpellier, France")

# Coordonnées de la Faculté des Sciences
fds_coord = [43.6312537,3.8612405]

# Créer une carte pour chaque jour de la semaine
days_of_week = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

for day in days_of_week:
    m = folium.Map(location=[43.6117, 3.8777], zoom_start=13)
    m.get_root().html.add_child(folium.Element(f"<h3 style='position: fixed; top: 10px; left: 10px; background-color: white; padding: 5px;'>Carte du {day}</h3>"))

    # Faculté des Sciences
    folium.Marker(
        location=fds_coord,
        popup="Faculté des Sciences",
        icon=Icon(icon="university", color="red", prefix="fa")
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

    # Dictionnaire associant les poids à des couleurs spécifiques
    couleurs_par_poids = {
        1: "#1f77b4",  # Bleu
        2: "#2ca02c",  # Vert
        3: "#FFFF00",  # Jaune
        4: "#ff7f0e",  # Orange
        5: "#d62728",  # Rouge
    }
    # Ecocompteurs
    for id, row in compteurs_df.iterrows():
        color = couleurs_par_poids.get(row['weight'])
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=8 + row['weight'],
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"Poids: {row['weight']}<br>Intensité: {row['intensity']}"
        ).add_to(m)
        
    # Chemins
    for route in paths:
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        folium.PolyLine(locations=route_coords, color='blue', weight=4, opacity=0.7).add_to(m)

    m.save(f"carte/map_montpellier_{day}.html")