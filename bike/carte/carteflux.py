import folium
from folium import Icon
import osmnx as ox
import pandas as pd

stations_df = pd.read_csv("https://drive.google.com/uc?id=1HgOLf2JD46ZJlyrF_c99QZb6of6ajNYh")

intensite = pd.read_csv("https://drive.google.com/uc?id=1WUCvXiGC-AEIR8oBWMiq7esZ5L05PU1M", sep=',')

# Contour de la ville
area = ox.geocode_to_gdf("Montpellier, France")

# Charger les pistes cyclables de Montpellier depuis OpenStreetMap
montpellier_graph = ox.graph_from_place("Montpellier, France", network_type="bike")
edges = ox.graph_to_gdfs(montpellier_graph, nodes=False)
edges = edges[~edges['highway'].isin(['footway', 'pedestrian', 'motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link'])]

#Créer une échelle de couleurs basée sur les intensités
min_intensity = intensite['intensite'].min()
max_intensity = intensite['intensite'].max()

# Poids et couleurs spécifiques associés
couleurs = {
    1: "#2ca02c",  # Vert
    2: "#FFFF00",  # Jaune
    3: "#ff7f0e",  # Orange
    4: "#d62728",  # Rouge
}

# Associer des couleurs aux routes cyclables
def get_closest_intensity(lat, lon, day_data):
    """
    Trouve l'intensité moyenne la plus proche pour une route donnée.

    Args:
        lat (float): Latitude du point.
        lon (float): Longitude du point.
        day_data (DataFrame): Données d'intensité pour un jour donné.

    Returns:
        float: Intensité la plus proche ou 0 si aucune donnée n'est trouvée.
    """
    if day_data.empty:
        print(f"Aucune donnée disponible pour les coordonnées ({lat}, {lon}).")
        return 0 
    #Trouver l'intensité moyenne la plus proche d'une route
    day_data = day_data.reset_index(drop=True)
    distances = ((day_data['latitude'] - lat) ** 2 + (day_data['longitude'] - lon) ** 2).pow(0.5)
    closest_index = distances.idxmin()
    if closest_index < 0 or closest_index >= len(day_data):
        print(f"Indice calculé ({closest_index}) introuvable dans les données.")
        return 0
    return day_data.iloc[closest_index]['intensite']

# Cartes pour chaque jour de la semaine
days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

for i, day in enumerate(days):
    """
    Crée une carte interactive pour un jour donné en fonction de l'intensité des routes.

    Étapes :
    - Ajout de la faculté des Sciences.
    - Tracé des contours de la ville.
    - Ajout des stations Velomagg.
    - Ajout des routes colorées en fonction des intensités.

    Enregistre une carte dans le répertoire `bike/carte`.
    """
    day_data = intensite[intensite['jour'] == day]
    edges['intensite'] = edges.apply(lambda row: get_closest_intensity(row.geometry.centroid.y, row.geometry.centroid.x, day_data), axis=1)
    
    mymap = folium.Map(location=[43.6117, 3.8767], zoom_start=13)

    # Faculté des Sciences
    folium.Marker(
        location=[43.6312537,3.8612405],
        popup="Faculté des Sciences",
        icon=Icon(icon="university", color="blue", prefix="fa")
    ).add_to(mymap)

    #Faculté de Droit et de Science Politique
    folium.Marker(
        location=[43.6145,3.8763],
        popup="Faculté de Droit et de Science Politiques",
        icon=Icon(icon="university", color="blue", prefix="fa")
    ).add_to(mymap)
    
    #Faculté Faculté d'Économie
    folium.Marker(
        location=[43.6096,3.8964],
        popup="Faculté Faculté d'Économie",
        icon=Icon(icon="university", color="blue", prefix="fa")
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

    # Stations Velomagg
    for id, row in stations_df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['nom'],
            icon=Icon(icon='bicycle', color='black', prefix='fa', icon_size=(15, 15))
        ).add_to(mymap)

    # Ajouter les routes cyclables colorées en fonction de l'intensité
    for _, row in edges.iterrows():
        if row['intensite'] <= 500:
            color = couleurs[1]  # Vert
        elif row['intensite'] <= 1000:
            color = couleurs[2]  # Jaune
        elif row['intensite'] <= 2000:
            color = couleurs[3]  # Orange
        else:
            color = couleurs[4]  # Rouge
            
        folium.PolyLine(
            locations=[(point[1], point[0]) for point in row['geometry'].coords],
            color=color,
            weight=3,
            opacity=0.8,
        ).add_to(mymap)
        
    mymap.save(f"docs/Carte/map_montpellier_{day}.html")