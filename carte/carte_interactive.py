import folium
import webbrowser

# Créer la carte centrée sur Montpellier
m = folium.Map(location=[43.6117, 3.8767], zoom_start=13)

# Exemple de stations (latitude, longitude)
stations = {
    "Station A": (43.6117, 3.8767),
    "Station B": (43.613, 3.880),
}

#dans la suite remplacer stations par la base de données de rokhaya
# Ajouter des marqueurs pour chaque station
for station, coords in stations.items():
    folium.Marker(location=coords, popup=station).add_to(m)

# Exemple de trajets (en reliant les stations)
folium.PolyLine(locations=[(43.6117, 3.8767), (43.613, 3.880)], color='blue', weight=2.5, opacity=1).add_to(m)

# Sauvegarder la carte sous forme de fichier HTML
file_path = "carte/map_velos.html"
m.save(file_path)

# Afficher la carte directement dans le notebook
webbrowser.open(file_path)
