# %%
# %%
import requests

def download_velomagg_data(url, output_filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_filename, 'wb') as file:
            file.write(response.content)
        print(f"Les données ont été téléchargées et enregistrées sous le nom : {output_filename}")
    else:
        print(f"Erreur lors du téléchargement des données. Code de statut : {response.status_code}")

# URL du fichier à télécharger
url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_Velomagg.csv"
# Nom du fichier de sortie
output_filename = "MMM_MMM_Velomagg.csv"

# Appel de la fonction pour télécharger le fichier
download_velomagg_data(url, output_filename)
#%%
import csv
from geopy.geocoders import Nominatim
import time

def get_coordinates(location_name, city):
    geolocator = Nominatim(user_agent="station_locator")
    try:
        location = geolocator.geocode(f"{location_name}, {city}, France")
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Erreur de géocodage pour {location_name}: {e}")
        return None, None

def process_stations(input_csv, output_csv):
    with open(input_csv, mode='r') as infile:
        reader = csv.DictReader(infile)
        fieldnames = ['\ufeffnom', 'latitude', 'longitude']
        stations_with_coords = []

        for row in reader:
            station_name = row.get('\ufeffnom', '').strip()
            city = row.get('commune', '').strip()
            
            if not station_name or not city:
                print(f"Informations incomplètes pour la ligne : {row}")
                continue
            
            lat, lon = get_coordinates(station_name, city)
            stations_with_coords.append({
                '\ufeffnom': station_name,
                'latitude': lat,
                'longitude': lon
            })
            time.sleep(1)  # Pour éviter de surcharger l'API

    with open(output_csv, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stations_with_coords)
        print(f"Fichier CSV avec les noms et les coordonnées créé : {output_csv}")

# Spécifiez les noms de fichiers
input_csv = 'MMM_MMM_Velomagg.csv'  # Nom du fichier d'entrée
output_csv = 'stations_with_coords.csv'  # Nom du fichier de sortie

# Appel de la fonction
process_stations(input_csv, output_csv)

# %%
