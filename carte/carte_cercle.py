import folium
from folium import Icon
import pandas as pd
import osmnx as ox

# Charger le contour de Montpellier
place_name = "Montpellier, France"
area = ox.geocode_to_gdf(place_name)



fds_coord = [43.6312537,3.8612405] # Coordonnées de la Faculté des Sciences de Montpellier
stations_df = pd.read_csv('Base_des_donnees/stations_velomagg.csv')


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






