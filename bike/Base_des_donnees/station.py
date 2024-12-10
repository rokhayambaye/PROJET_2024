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
from geopy.geocoders import Nominatim
import time
import pandas as pd

# Chargement des données des stations VéloMagg
MMM_MMM_Velomagg = pd.read_csv("https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_Velomagg.csv", encoding="utf-8")

def obtenir_coordonnees(nom_lieu, ville):
    """
    Cette fonction nous permet d'obtenir les coordonnées géographiques (latitude et longitude) d'un lieu donné.

    Paramètres :
    -----------
    nom_lieu : str
        le nom du lieu ou de la station
    ville : str
        Le nom de la ville associé au lieu.

    Sortie :
    ---------
    tuple
        Retourne un tuple contenant la latitude et la longitude du lieu et renvoie (None, None) si les coordonnées ne peuvent pas être trouvées  .

    Exceptions :
    -----------
    Affiche une message d'erreur en cas d'un erreur de géocodage et retoune (None,None).
    """
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
    """
    Traite un DataFrame de stations et ajoute les coordonnées géographiques.

    Cette fonction parcourt les lignes d'un DataFrame contenant les noms des
    stations et leurs villes associées, utilise le service Geopy pour obtenir
    leurs coordonnées géographiques, et retourne une liste de dictionnaires
    avec les résultats.

    Paramètres :
    -----------
    dataframe : pandas.DataFrame
        Un Dataframe contenant au moins les colonnes 'nom' et 'commune' .
    Sortie :
    ---------
    Renvoie une liste contenant :
        - 'nom' : Le nom de la station.
        - 'latitude' : La latitude de la station.
        - 'longitude' : La longitude de la station.

    Notes :
    ------
    - La fonction utilise un délai de 1 seconde entre les appels à l'API Geopy
      pour respecter les limites de fréquence d'utilisation.
    - Les lignes manquant des données sont ignorées ,
      avec un message affiché pour chaque cas .
    """
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
