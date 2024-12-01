import csv
from geopy.geocoders import Nominatim
import time
import pandas as pd


MMM_MMM_Velomagg = pd.read_csv("https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_Velomagg.csv", encoding="utf-8")

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

def process_stations(dataframe):
    stations_with_coords = []

    for _, row in dataframe.iterrows():
        station_name = row.get('nom', '').strip()
        city = row.get('commune', '').strip()
            
        if not station_name or not city:
            print(f"Informations incomplètes pour la ligne : {row}")
            continue
            
        lat, lon = get_coordinates(station_name, city)
        stations_with_coords.append({
            'nom': station_name,
            'latitude': lat,
            'longitude': lon
        })
        time.sleep(1)  # Pour éviter de surcharger l'API

stations_with_coords = process_stations(MMM_MMM_Velomagg)
