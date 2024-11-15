#%%
import osmnx as ox
import networkx as nx
import folium
from folium import Icon
import pandas as pd
from datetime import datetime
from matplotlib import cm
from matplotlib.colors import Normalize

# Fonction pour obtenir le jour de la semaine en toutes lettres
def get_weekday_name():
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    return days[datetime.now().weekday()]  # Renvoie le nom du jour actuel

# Associer une couleur à chaque jour de la semaine
def get_day_color(day_name):
    colors = {
        "Lundi": "blue",
        "Mardi": "green",
        "Mercredi": "orange",
        "Jeudi": "purple",
        "Vendredi": "red",
        "Samedi": "brown",
        "Dimanche": "pink"
    }
    return colors.get(day_name, "black")  # Retourne la couleur par défaut (noir) si le jour n'est pas trouvé

stations_df = pd.read_csv('carte/stations_velomagg.csv')
stations_coords = stations_df[['Latitude', 'Longitude']].values

# Associer un poids à une intervalle de valeurs d'intensité
# Liste d'intervalles et leurs poids associés
poids_par_intervalles = [
    ((0, 100), 1), 
    ((100, 200), 2),  
    ((200, 300), 3) 
]
# Fonction pour trouver le poids d'une valeur donnée
def poids(valeur):
    for (a, b), poids in poids_par_intervalles:
        if a <= valeur < b:
            return poids
    return 0
# TEST
data = {
    "Nom": ["Station A", "Station B", "Station C", "Station D", "Station E"],
    "Latitude": [43.610, 43.611, 43.612, 43.613, 43.614],
    "Longitude": [3.876, 3.877, 3.878, 3.879, 3.880],
    "Intensité": [15, 120, 245, 30, 75]
}
# Créer le DataFrame
compteurs_df = pd.DataFrame(data)
compteurs_df['Poids'] = compteurs_df['Intensité'].apply(poids)

# Normaliser les poids
norm = Normalize(vmin=min(p[1] for p in poids_par_intervalles),
                 vmax=max(p[1] for p in poids_par_intervalles))

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


# Obtenir le contour de la ville de Montpellier
place_name = "Montpellier, France"
area = ox.geocode_to_gdf(place_name)

fds_coord = [43.6312537,3.8612405] # Coordonnées de la Faculté des Sciences de Montpellier


days_of_week = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# Créer une carte pour chaque jour de la semaine
for day in days_of_week:
    m = folium.Map(location=[43.6117, 3.8777], zoom_start=13)
    m.get_root().html.add_child(folium.Element(f"<h3 style='position: fixed; top: 10px; left: 10px; background-color: white; padding: 5px;'>Carte du {day}</h3>"))

    # Ajouter un marqueur pour la Faculté des Sciences
    folium.Marker(
        location=fds_coord,
        popup="Faculté des Sciences",
        icon=Icon(icon="university", color="RED", prefix="fa")
    ).add_to(m)

 # Ajouter le contour de la ville avec une bordure noire
    folium.GeoJson(
        data=area["geometry"],
        style_function=lambda x: {
            "color": "black",
            "weight": 2,
        }
    ).add_to(m)

    # Ajouter les stations à la carte avec leurs noms
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
        lat, lon = row['Latitude'], row['Longitude']
        station_name = row['Nom']
        folium.Marker(location=[lat, lon], popup=station_name, icon=Icon(icon='bicycle', color='black', prefix='fa', icon_size=(20, 20))).add_to(m)

    # Tracer les chemins passant par les stations avec des couleurs différentes selon le jour
    day_color = get_day_color(day)  # Récupère la couleur associée au jour
    for route in paths:
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        folium.PolyLine(locations=route_coords, color=day_color, weight=4, opacity=0.7).add_to(m)

m.save(f"carte/map_montpellier_{day}.html")


# Créer une carte avec les cercles de temps 
MAP_MTP = folium.Map(location=[43.6117, 3.8777], zoom_start=13)

# Ajouter un marqueur pour la Faculté des Sciences
folium.Marker(
    location=fds_coord,
    popup="Faculté des Sciences",
    icon=Icon(icon="university", color="blue", prefix="fa")
).add_to(MAP_MTP)

# Ajouter les cercles de temps de trajet autour de la Faculté des Sciences
folium.Circle(
    location=fds_coord,
    radius=1250,  # Moins de 5 minutes
    color="green",
    fill=True,
    fill_opacity=0.1,
    popup="Moins de 5 minutes en vélo"
).add_to(MAP_MTP)

folium.Circle(
    location=fds_coord,
    radius=2500,  # Moins de 10 minutes
    color="orange",
    fill=True,
    fill_opacity=0.1,
    popup="Moins de 10 minutes en vélo"
).add_to(MAP_MTP)

folium.Circle(
    location=fds_coord,
    radius=5000,  # Moins de 20 minutes
    color="red",
    fill=True,
    fill_opacity=0.1,
    popup="Moins de 20 minutes en vélo"
).add_to(MAP_MTP)

# Ajouter toutes les stations à la carte
for id, row in stations_df.iterrows():
    lat, lon = row['Latitude'], row['Longitude']
    station_name = row['Nom']
    folium.Marker(
        location=[lat, lon],
        popup=station_name,
        icon=Icon(icon='bicycle', color='black', prefix='fa', icon_size=(20, 20))
    ).add_to(MAP_MTP)

# Ajouter le contour de la ville
folium.GeoJson(
    data=area["geometry"],
    style_function=lambda x: {
        "fillColor": "black",
        "color": "black",
        "weight": 2,
        "fillOpacity": 0.08,
    }
).add_to(MAP_MTP)

# Enregistrer la carte supplémentaire
MAP_MTP.save("carte/map_montpellier.html")






