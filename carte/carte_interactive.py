import folium
import webbrowser
import pandas as pd

# Charger les données depuis le fichier CSV
# Assurez-vous que le fichier CSV se trouve dans le même répertoire ou spécifiez le chemin complet.
stations_df = pd.read_csv("carte/stations_velomagg.csv")  # Assurez-vous d'avoir un fichier stations.csv avec les colonnes: nom, latitude, longitude

# Créer la carte centrée sur Montpellier
m = folium.Map(location=[43.6117, 3.8767], zoom_start=13)

# Ajouter des marqueurs pour chaque station à partir du DataFrame
for index, row in stations_df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=row['Nom']
    ).add_to(m)

# Ajouter un exemple de trajet entre deux stations (si nécessaire)
# Sinon, utilisez une boucle pour créer des trajets entre plusieurs stations
if len(stations_df) > 1:  # Vérifiez qu'il y a au moins 2 stations pour créer un trajet
    coords = list(zip(stations_df['Latitude'], stations_df['Longitude']))
    folium.PolyLine(locations=coords, color='blue', weight=2.5, opacity=1).add_to(m)

# Sauvegarder la carte sous forme de fichier HTML
file_path = "carte/map_velos.html"
m.save(file_path)

# Ouvrir la carte dans le navigateur
webbrowser.open(file_path)
