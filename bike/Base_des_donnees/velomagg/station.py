import csv
from geopy.geocoders import Nominatim
import time
import pandas as pd

MMM_MMM_Velomagg = pd.read_csv("https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_Velomagg.csv", encoding="utf-8")

def get_coordinates(location_name, city):
    """
    Récupère les coordonnées géographiques (latitude, longitude) d'un lieu spécifié.

    Cette fonction utilise l'API Nominatim de `geopy` pour effectuer une recherche de géolocalisation
    basée sur le nom d'un lieu et une ville, et renvoie les coordonnées correspondantes.

    Args:
        location_name (str): Nom du lieu pour lequel on souhaite obtenir les coordonnées.
        city (str): Ville où se trouve le lieu.

    Returns:
        tuple: Un tuple contenant la latitude et la longitude du lieu, ou (None, None) si la géolocalisation échoue.
    
    Example:
        >>> get_coordinates("Place de la Comédie", "Montpellier")
        (43.611746, 3.876716)
    """
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
    """
    Traite un dataframe de stations pour obtenir leurs coordonnées géographiques.

    Cette fonction parcourt chaque ligne du dataframe, extrait les informations sur le nom de la station
    et la ville, puis utilise la fonction `get_coordinates` pour obtenir les coordonnées (latitude, longitude)
    correspondantes. Elle retourne ensuite une liste de dictionnaires contenant ces informations.

    Args:
        dataframe (pd.DataFrame): Un dataframe contenant des informations sur les stations,
                                  avec au minimum les colonnes 'nom' et 'commune'.

    Returns:
        list: Une liste de dictionnaires où chaque dictionnaire contient les éléments suivants :
              - 'nom' (str): Le nom de la station.
              - 'latitude' (float): La latitude de la station.
              - 'longitude' (float): La longitude de la station.

    Example:
        >>> stations_with_coords = process_stations(MMM_MMM_Velomagg)
        >>> print(stations_with_coords[0])
        {'nom': 'Place de la Comédie', 'latitude': 43.611746, 'longitude': 3.876716}
    """
    stations_with_coords = []

    for _, row in dataframe.iterrows():
        station_name = row.get('nom', '').strip()
        city = row.get('commune', '').strip()
            
        if not station_name or not city:
            print(f"Informations manquantes pour la ligne : {row}")
            continue
            
        lat, lon = get_coordinates(station_name, city)
        stations_with_coords.append({
            'nom': station_name,
            'latitude': lat,
            'longitude': lon
        })
        time.sleep(1)  # Respect de la limite de fréquence de l'API

    return stations_with_coords
