import folium
from folium import Icon
import osmnx as ox
import pandas as pd
import branca.colormap as cm


stations_df = pd.read_csv('Base_des_donnees/stations_velomagg.csv')
stations_coords = stations_df[['Latitude', 'Longitude']].values


# Contour de la ville
area = ox.geocode_to_gdf("Montpellier, France")

# Charger les données des éco-compteurs
file_path = 'Base_des_donnees/donnees_montpellier_2023.csv'  
Donnees_montpellier = pd.read_csv(file_path, sep=';')

# Convertir la colonne 'date' en datetime
Donnees_montpellier['date'] = pd.to_datetime(Donnees_montpellier['date'])

# Regrouper les intensités par coordonnées pour calculer les moyennes
intensites = Donnees_montpellier.groupby(['latitude', 'longitude'])['intensity'].mean().reset_index()

# Charger les pistes cyclables de Montpellier depuis OpenStreetMap
montpellier_graph = ox.graph_from_place("Montpellier, France", network_type="bike")
edges = ox.graph_to_gdfs(montpellier_graph, nodes=False)

# Créer une échelle de couleurs basée sur les intensités
min_intensity = intensites['intensity'].min()
max_intensity = intensites['intensity'].max()
colormap = cm.linear.YlOrRd_09.scale(min_intensity, max_intensity)


# Associer des couleurs aux routes cyclables (en fonction des intensités les plus proches)
def get_closest_intensity(lat, lon):
    """Trouver l'intensité moyenne la plus proche d'une route."""
    distances = ((intensites['latitude'] - lat) ** 2 + (intensites['longitude'] - lon) ** 2).pow(0.5)
    closest_index = distances.idxmin()
    return intensites.iloc[closest_index]['intensity']

edges['intensity'] = edges.apply(
    lambda row: get_closest_intensity(row.geometry.centroid.y, row.geometry.centroid.x), axis=1
)

# Créer la carte centrée sur Montpellier
montpellier_coords = [43.6117, 3.8767]
mymap = folium.Map(location=montpellier_coords, zoom_start=13)

# Ajouter les routes cyclables colorées en fonction de l'intensité
for _, row in edges.iterrows():
    folium.PolyLine(
        locations=[(point[1], point[0]) for point in row['geometry'].coords],
        color=colormap(row['intensity']),
        weight=3,
        opacity=0.8,
    ).add_to(mymap)

# Stations Velomagg
for id, row in stations_df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=row['Nom'],
        icon=Icon(icon='bicycle', color='black', prefix='fa', icon_size=(15, 15))
    ).add_to(mymap)

# Contour de la ville
folium.GeoJson(
    data=area["geometry"],
    style_function=lambda x: {
        "color": "black",
        "weight": 2,
        "fillOpacity": 0
    }
    ).add_to(mymap)

# Ajouter une légende
colormap.caption = "Intensité des vélos (éco-compteurs)"
colormap.add_to(mymap)

# Sauvegarder la carte
mymap.save("carte/carte_pistes_cyclables_intensites.html")
