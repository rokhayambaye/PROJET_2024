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
print(df_stations)

df_stations= df_stations [df_stations['Nom'] != 'Station sans nom'] #Suppresion des stations sans nom
print(df_stations)

df_stations.to_csv("carte/stations_velomagg.csv", index=False)
