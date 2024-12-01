#%%
import osmnx as ox
import networkx as nx
import folium
from folium import Icon
import pandas as pd
import geopandas as gpd
from datetime import datetime
from matplotlib import cm
from matplotlib.colors import Normalize
import shapely
from shapely.geometry import Point

stations_df = pd.read_csv('Base_des_donnees/stations_velomagg.csv')
stations_coords = stations_df[['Latitude', 'Longitude']].values

compteurs_df = pd.read_csv('Base_des_donnees/moyenne_intensite.csv')

G = ox.graph_from_place( "Montpellier, France", network_type='bike')

# Contour de la ville
area = ox.geocode_to_gdf("Montpellier, France")

# Coordonnées de la Faculté des Sciences
fds_coord = [43.6312537,3.8612405]

# Extraire le polygone de Montpellier
montpellier_polygon = area["geometry"].iloc[0]  # Polygone principal

# Vérifier si chaque écocompteur est dans Montpellier
compteurs_df['inside'] = compteurs_df.apply(
    lambda row: montpellier_polygon.contains(Point(row['longitude'], row['latitude'])),
    axis=1
)

# Ne conserver que les écocompteurs dans Montpellier
compteurs_df = compteurs_df[compteurs_df['inside']]

routes = gpd.read_file('Base_des_donnees/export.geojson')
routes = routes.to_crs(epsg=32631)

# Intervalles et Poids associés par tranche de 500
poids_par_intervalles = [
    ((0, 500), 1), 
    ((500, 1000), 2),  
    ((1000, 1500), 3),
    ((1500, 2000), 4),
    ((2000, 2500), 5),
]

def poids(valeur):
    for (a, b), poids in poids_par_intervalles:
        if a <= valeur < b:
            return poids
    return 0

# Ajout colonne Poids 
compteurs_df['poids'] = compteurs_df['intensite'].apply(poids)

# Normaliser les poids
norm = Normalize(vmin=min(p[1] for p in poids_par_intervalles),
                 vmax=max(p[1] for p in poids_par_intervalles))

# Noeuds les plus proches
stations_nodes = []
for id, row in stations_df.iterrows():
    lat, lon = row['Latitude'], row['Longitude']
    node = ox.distance.nearest_nodes(G, X=lon, Y=lat)
    stations_nodes.append((node, row['Nom']))

# Chemins entre les stations (par pairs)
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
        
# Carte pour chaque jour de la semaine
days_of_week = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

for i, day in enumerate(days_of_week):
    day_data = compteurs_df[compteurs_df['jour'] == day]
    
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

    # Poids et couleurs spécifiques associés
    couleurs = {
        1: "#1f77b4",  # Bleu
        2: "#2ca02c",  # Vert
        3: "#FFFF00",  # Jaune
        4: "#ff7f0e",  # Orange
        5: "#d62728",  # Rouge
    }
    
    # Ecocompteurs
    for id, row in day_data.iterrows():
        color = couleurs.get(row['poids'])
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=8 + row['poids'],
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"Intensité: {row['intensite']} au {day}"
        ).add_to(m)

    # Chemins
    circuit = gpd.GeoDataFrame(
        day_data,
        geometry = [Point(lon, lat) for lon, lat in zip(day_data['longitude'], day_data['latitude'])],
        crs="EPSG:4326"
    )
    circuit = circuit.to_crs(epsg=32631)
    join = gpd.sjoin_nearest(routes,circuit, how="inner", max_distance=100)
    
    # Ajouter les polylignes sur la carte
    for _, row in join.iterrows():
        route_color = 'blue'
        if isinstance(row.geometry, shapely.geometry.LineString):
            coords = [[p[1], p[0]] for p in list(row.geometry.coords)]
        elif isinstance(row.geometry, shapely.geometry.Polygon):
            coords = [[p[1], p[0]] for p in list(row.geometry.exterior.coords)]
        else:
            continue

        folium.PolyLine(
            locations=coords,
            color=route_color,
            weight=5
        ).add_to(m)

    m.save(f"carte/map_montpellier_{day}.html")