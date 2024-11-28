# %%
import pandas as pd
import folium
from moviepy import ImageSequenceClip
import numpy as np
import os
import shutil

# Charger les données
data = pd.read_csv("Velomagg_2023_with_coords.csv")
# Supprimer les lignes avec des NaN dans les coordonnées
data = data.dropna(subset=['departure_latitude', 'departure_longitude', 'return_latitude', 'return_longitude'])
data['Departure'] = pd.to_datetime(data['Departure'])
data['Return'] = pd.to_datetime(data['Return'])
data = data.sort_values(by='Departure')

# Créer un dossier pour sauvegarder les frames
output_dir = "frames"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

# Fonction pour créer une carte de base
def create_base_map():
    return folium.Map(location=[43.6117, 3.8777], zoom_start=13, tiles="OpenStreetMap")

# Fonction pour calculer la position intermédiaire des vélos
def interpolate_position(lat1, lon1, lat2, lon2, alpha):
    """
    Calcule une position intermédiaire entre deux points.
    alpha : proportion du trajet effectué (de 0 à 1)
    """
    lat = lat1 + (lat2 - lat1) * alpha
    lon = lon1 + (lon2 - lon1) * alpha
    return lat, lon

# Fonction pour ajouter des vélos en mouvement à un instant donné
def add_moving_bikes(map_object, data, current_time):
    for _, row in data.iterrows():
        if row['Departure'] <= current_time <= row['Return']:
            # Calculer la proportion du trajet effectué
            total_time = (row['Return'] - row['Departure']).total_seconds()
            elapsed_time = (current_time - row['Departure']).total_seconds()
            alpha = elapsed_time / total_time  # Proportion de 0 à 1

            # Calculer la position intermédiaire
            lat, lon = interpolate_position(
                row['departure_latitude'], row['departure_longitude'],
                row['return_latitude'], row['return_longitude'],
                alpha
            )

            # Ajouter un point à la position intermédiaire
            folium.CircleMarker(
                location=[lat, lon],
                radius=5,
                color="blue",
                fill=True,
                fill_color="blue",
                fill_opacity=0.8,
            ).add_to(map_object)

# Générer les frames pour l'animation
timestamps = pd.date_range(data['Departure'].min(), data['Return'].max(), freq='1H')
for i, timestamp in enumerate(timestamps):
    base_map = create_base_map()
    add_moving_bikes(base_map, data, timestamp)
    base_map.save(f"{output_dir}/frame_{i:04d}.html")

    # Convertir le HTML en image avec Selenium
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(800, 600)
    driver.get(f"file://{os.getcwd()}/{output_dir}/frame_{i:04d}.html")
    driver.save_screenshot(f"{output_dir}/frame_{i:04d}.png")
    driver.quit()

# Créer une vidéo à partir des frames
frames = [f"{output_dir}/frame_{i:04d}.png" for i in range(len(timestamps))]
clip = ImageSequenceClip(frames, fps=1)
clip.write_videofile("bike_traffic_moving_points.mp4", codec="libx264")

# Nettoyer les fichiers temporaires
shutil.rmtree(output_dir)

# %%

# %%
#creation video de 1 min

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import geopandas as gpd

# Charger les données
data = pd.read_csv("Velomagg_2023_with_coords.csv")

# Convertir la colonne departure_time en datetime
data['Departure'] = pd.to_datetime(data['Departure'])

# Extraire l'heure de départ pour l'analyse
data['hour'] = data['Departure'].dt.hour

# Analyse des moments de la journée
hourly_counts = data['hour'].value_counts().sort_index()

# Visualisation des moments de la journée
plt.figure(figsize=(10, 6))
plt.plot(hourly_counts.index, hourly_counts.values, marker='o', linestyle='-')
plt.title("Répartition des trajets par heure de la journée")
plt.xlabel("Heure")
plt.ylabel("Nombre de trajets")
plt.xticks(range(0, 24))  # Assurer une échelle de 0 à 23 heures
plt.grid()
plt.show()

# Charger un fond de carte (par exemple, de Montpellier)
montpellier_map = gpd.read_file("montpellier_shapefile.shp")

# Créer une figure pour l'animation
fig, ax = plt.subplots(figsize=(10, 10))
montpellier_map.plot(ax=ax, color='lightgrey')

# Nombre de frames pour 1 minute de vidéo à 30 fps
frames = 1800
interval = 1000 / 30  # 30 images par seconde

# Fonction pour mettre à jour l'animation
def update(frame):
    ax.clear()
    montpellier_map.plot(ax=ax, color='lightgrey')
    
    # Calcul du temps actuel en fonction du nombre de frames
    current_time = data['departure_time'].min() + pd.Timedelta(minutes=(frame / 30))  # 1 frame = 1/30 minute
    
    active_trips = data[(data['Departure'] <= current_time) & (data['Return'] >= current_time)]
    
    # Ajouter les vélos en mouvement
    for _, trip in active_trips.iterrows():
        lat = [trip['departure_latitude'], trip['return_latitude']]
        lon = [trip['departure_longitude'], trip['return_longitude']]
        ax.plot(lon, lat, color='blue', alpha=0.5)
        ax.scatter(trip['departure_longitude'], trip['departure_latitude'], color='red', s=10)

# Créer l'animation
anim = FuncAnimation(fig, update, frames=frames, interval=interval)

# Sauvegarder l'animation en vidéo (MP4)
anim.save("montpellier_bike_traffic_1min.mp4", writer='ffmpeg', fps=30)

print("La vidéo d'une minute a été créée avec succès !")
# %%
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import osmnx as ox

# Charger les données des trajets
data = pd.read_csv("Velomagg_2023_with_coords.csv")

# Convertir les colonnes de temps en datetime
data['Departure'] = pd.to_datetime(data['Departure'])
data['Return'] = pd.to_datetime(data['Return'])

# Extraire l'heure de départ pour l'analyse
data['hour'] = data['Departure'].dt.hour

# Analyse des moments de la journée
hourly_counts = data['hour'].value_counts().sort_index()

# Visualisation des moments de la journée
plt.figure(figsize=(10, 6))
plt.plot(hourly_counts.index, hourly_counts.values, marker='o', linestyle='-')
plt.title("Répartition des trajets par heure de la journée")
plt.xlabel("Heure")
plt.ylabel("Nombre de trajets")
plt.xticks(range(0, 24))  # Assurer une échelle de 0 à 23 heures
plt.grid()
plt.show()

# Charger automatiquement la carte de Montpellier avec osmnx
montpellier_map = ox.graph_from_place("Montpellier, France", network_type="all")

# Convertir la carte en GeoDataFrame pour le tracé
nodes, edges = ox.graph_to_gdfs(montpellier_map)

# Créer une figure pour l'animation
fig, ax = plt.subplots(figsize=(10, 10))

# Tracer les rues de Montpellier en fond de carte
edges.plot(ax=ax, color='lightgrey', linewidth=0.5)

# Paramètres pour l'animation
frames = 1800  # 1 minute d'animation à 30 fps
interval = 1000 / 30  # Intervalle entre les frames (en ms)

# Fonction pour mettre à jour l'animation
def update(frame):
    ax.clear()
    edges.plot(ax=ax, color='lightgrey', linewidth=0.5)  # Fond de carte
    
    # Calcul du temps actuel en fonction du nombre de frames
    current_time = data['Departure'].min() + pd.Timedelta(minutes=(frame / 30))  # 1 frame = 1/30 minute
    
    # Filtrer les trajets actifs à l'heure actuelle
    active_trips = data[(data['Departure'] <= current_time) & (data['Return'] >= current_time)]
    
    # Ajouter les vélos en mouvement
    for _, trip in active_trips.iterrows():
        lat = [trip['departure_latitude'], trip['return_latitude']]
        lon = [trip['departure_longitude'], trip['return_longitude']]
        ax.plot(lon, lat, color='blue', alpha=0.5)
        ax.scatter(trip['departure_longitude'], trip['departure_latitude'], color='red', s=10)
    
    # Ajouter un titre avec l'heure actuelle
    ax.set_title(f"Circulation des vélos à Montpellier\n{current_time.strftime('%Y-%m-%d %H:%M:%S')}", fontsize=14)

# Créer l'animation
anim = FuncAnimation(fig, update, frames=frames, interval=interval)

# Sauvegarder l'animation en vidéo (MP4)
anim.save("montpellier_bike_traffic_1min.mp4", writer='ffmpeg', fps=30)

print("La vidéo d'une minute a été créée avec succès !")

# %%
import requests
import pandas as pd

# URL de l'API (exemple hypothétique)
api_url = "https://data.montpellier3m.fr/api/velomagg/trips"

# Paramètres pour un jour spécifique
params = {
    "date": "2020-01-02",  # Date souhaitée (au format AAAA-MM-JJ)
    "apikey": "VOTRE_CLE_API"  # Remplacez par votre clé API si nécessaire
}

# Requête API
response = requests.get(api_url, params=params)

# Vérifier la réponse
if response.status_code == 200:
    # Charger les données dans un DataFrame
    data = pd.DataFrame(response.json())
    print("Données récupérées :", data.head())
    
    # Sauvegarder les données en CSV
    data.to_csv("velomagg_2024-11-26.csv", index=False)
    print("Fichier CSV enregistré.")
else:
    print("Erreur lors de la récupération des données :", response.status_code)

# %%
