import requests
import pandas as pd

# Définir la requête Overpass
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
area["name"="Montpellier"]->.searchArea;
node["amenity"="bicycle_rental"](area.searchArea);
out body;
"""

# Envoyer la requête
response = requests.get(overpass_url, params={'data': overpass_query})
data = response.json()

# Extraire les informations de latitude et de longitude
stations = []
for element in data['elements']:
    lat = element['lat']
    lon = element['lon']
    name = element.get('tags', {}).get('name', 'Station sans nom')
    stations.append({'Nom': name, 'Latitude': lat, 'Longitude': lon})

# Convertir en DataFrame pour une meilleure visualisation
df_stations = pd.DataFrame(stations)

df_stations= df_stations [df_stations['Nom'] != 'Station sans nom'] #Suppresion des stations sans nom

# Liste des stations à retirer
stations_a_retirer = ["Seb éco", "Palavas Sport", "Le Galexia", "Galexia", "Paulette", "Bikemed","Parking du Tramway Saint-Jean de Védas","Jacou",
                      "Vélomagg plage","Notre-Dame de Sablassou","Lattes Centre"]

# Filtrer le DataFrame pour conserver uniquement les stations qui ne sont pas dans la liste
df_stations =df_stations[~df_stations['Nom'].isin(stations_a_retirer)]

df_stations.to_csv("Base_des_donnees/stations_velomagg.csv", index=False)

print(df_stations)
