from geopy.geocoders import Nominatim
import time
import pandas as pd

MMM_MMM_Velomagg = pd.read_csv("https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_Velomagg.csv", encoding="utf-8")

def obtenir_coordonnees(nom_lieu, ville):
    geolocator = Nominatim(user_agent="station_locator")
    try:
        location = geolocator.geocode(f"{nom_lieu}, {ville}, France")
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Erreur de géocodage pour {nom_lieu}: {e}")
        return None, None

def traiter_stations(dataframe):
    stations_avec_coordonnees = []

    for _, row in dataframe.iterrows():
        nom_station = row.get('nom', '').strip()
        ville = row.get('commune', '').strip()
            
        if not nom_station or not ville:
            print(f"Informations manquantes pour la ligne : {row}")
            continue
            
        lat, lon = obtenir_coordonnees(nom_station, ville)
        stations_avec_coordonnees.append({
            'nom': nom_station,
            'latitude': lat,
            'longitude': lon
        })
        time.sleep(1)  # Respect de la limite de fréquence de l'API

    return stations_avec_coordonnees
