import pandas as pd

# Chargement des données des stations avec leurs coordonnées
stations_df = pd.read_csv("https://drive.google.com/uc?id=1VGH928Tt0TrrrJb2mIdHrybvLSCkziFi")  
stations_dict = stations_df.set_index('nom')[['latitude', 'longitude']].to_dict(orient='index')

# Chargement des données de trajets
trips_df = pd.read_csv("https://drive.google.com/uc?id=15tH6-xdxTAVr5KTnfPrxfQLObMyD9bew") 

# Ajout des coordonnées pour les stations de départ et d'arrivée
def get_lat_lon(station_name):
    if station_name in stations_dict:
        return stations_dict[station_name]['latitude'], stations_dict[station_name]['longitude']
    else:
        return None, None

trips_df['departure_latitude'], trips_df['departure_longitude'] = zip(*trips_df['Departure station'].apply(get_lat_lon))
trips_df['return_latitude'], trips_df['return_longitude'] = zip(*trips_df['Return station'].apply(get_lat_lon))