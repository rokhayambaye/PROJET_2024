#%%
import pandas as pd

# Chargement des données des stations avec leurs coordonnées
stations_df = pd.read_csv('stations_with_coords.csv')  # Fichier des stations avec coordonnées
stations_dict = stations_df.set_index('nom')[['latitude', 'longitude']].to_dict(orient='index')

# Chargement des données de trajets
trips_df = pd.read_csv('Velomagg_2023.csv')  # Remplacez par le nom de votre fichier de trajets

# Ajout des colonnes de latitude et longitude pour les stations de départ et d'arrivée
def get_lat_lon(station_name):
    if station_name in stations_dict:
        return stations_dict[station_name]['latitude'], stations_dict[station_name]['longitude']
    else:
        return None, None

trips_df['departure_latitude'], trips_df['departure_longitude'] = zip(*trips_df['Departure station'].apply(get_lat_lon))
trips_df['return_latitude'], trips_df['return_longitude'] = zip(*trips_df['Return station'].apply(get_lat_lon))

# Sauvegarde du fichier de sortie avec les nouvelles colonnes
output_file = 'Velomagg_2023_with_coords.csv'
trips_df.to_csv(output_file, index=False)
print(f"Fichier avec les coordonnées ajouté : {output_file}")
# %%
