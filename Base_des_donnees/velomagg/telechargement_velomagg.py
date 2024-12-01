import pandas as pd
import seaborn as sns 

sns.set_palette("colorblind")
palette = sns.color_palette("twilight", n_colors=12)
pd.options.display.max_rows = 8

Velomagg = pd.read_csv("https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_CoursesVelomagg.csv")

# Remplacer spécifiquement 'Deux Ponts - Gare Saint-Roch' par 'Deux Ponts Gare Saint-Roch' dans le DataFrame velomagg_2023
Velomagg['Departure station'] = Velomagg['Departure station'].str.replace('Ã©', 'é')
Velomagg['Return station'] = Velomagg['Return station'].str.replace('Ã©', 'é')
Velomagg['Departure station'] = Velomagg['Departure station'].str.replace('Ã¨', 'è')
Velomagg['Return station'] = Velomagg['Return station'].str.replace('Ã¨', 'è')
Velomagg['Departure station'] = Velomagg['Departure station'].str.replace('Ã´', 'ô')
Velomagg['Return station'] = Velomagg['Return station'].str.replace('Ã´', 'ô')

# Suppression des chiffres et des espaces devant les noms des stations
Velomagg['Departure station'] = Velomagg['Departure station'].str.replace(r'^\d+\s*', '', regex=True)
Velomagg['Return station'] = Velomagg['Return station'].str.replace(r'^\d+\s*', '', regex=True)
Velomagg['Departure station'] =Velomagg['Departure station'].str.replace('Antigone centre', 'Antigone Centre')
Velomagg['Return station'] =Velomagg['Return station'].str.replace('Antigone centre',  'Antigone Centre')
Velomagg['Departure station'] =Velomagg['Departure station'].str.replace('Fac de Lettres', 'Fac des Sciences')
Velomagg['Return station'] =Velomagg['Return station'].str.replace('Fac de Lettres',  'Fac des Sciences')
Velomagg['Departure station'] =Velomagg['Departure station'].str.replace('Perols etang or', 'Pérols')
Velomagg['Return station'] =Velomagg['Return station'].str.replace('Perols etang or',  'Pérols')
Velomagg['Departure station'] =Velomagg['Departure station'].str.replace("Pérols Etang de l'Or", 'Pérols')
Velomagg['Return station'] =Velomagg['Return station'].str.replace("Pérols Etang de l'Or",  'Pérols')
Velomagg['Departure station'] =Velomagg['Departure station'].str.replace('Sud De France', 'Montpellier Sud de France')
Velomagg['Return station'] =Velomagg['Return station'].str.replace('Sud De France',  'Montpellier Sud de France')
Velomagg['Departure station'] =Velomagg['Departure station'].str.replace('Albert 1er - Cathédrale', 'Albert 1er - Cathedrale')
Velomagg['Return station'] =Velomagg['Return station'].str.replace('Albert 1er - Cathédrale',  'Albert 1er - Cathedrale')
Velomagg['Departure station'] =Velomagg['Departure station'].str.replace('Place Albert 1er - St Charles', 'Place Albert 1er - St-Charles')
Velomagg['Return station'] =Velomagg['Return station'].str.replace('Place Albert 1er - St Charles',  'Place Albert 1er - St-Charles')
Velomagg['Departure station'] =Velomagg['Departure station'].str.replace('Pont de Lattes - Gare Saint-Roch', 'Pont de Lattes - Gare St-Roch')
Velomagg['Return station'] =Velomagg['Return station'].str.replace('Pont de Lattes - Gare Saint-Roch',  'Pont de Lattes - Gare St-Roch')
Velomagg['Departure station'] =Velomagg['Departure station'].str.replace('Rue Jules Ferry - Gare Saint-Roch', 'Rue Jules Ferry')
Velomagg['Return station'] =Velomagg['Return station'].str.replace('Rue Jules Ferry - Gare Saint-Roch',  'Rue Jules Ferry')
Velomagg['Departure station'] =Velomagg['Departure station'].str.replace('Parvis Jules Ferry - Gare Saint-Roch', 'Parvis Jules Ferry')
Velomagg['Return station'] =Velomagg['Return station'].str.replace('Parvis Jules Ferry - Gare Saint-Roch',  'Parvis Jules Ferry')
Velomagg['Departure station'] =Velomagg['Departure station'].str.replace("Prés d'Arènes",  "Près d'Arènes")
Velomagg['Return station'] =Velomagg['Return station'].str.replace("Prés d'Arènes", "Près d'Arènes")
Velomagg['Departure station'] =Velomagg['Departure station'].str.replace("Providence - Ovalie",  "Providence-Ovalie")
Velomagg['Return station'] =Velomagg['Return station'].str.replace("Providence - Ovalie", "Providence-Ovalie")

# Colonnes souhaitées
columns =['Departure station', 'Departure', 'Return station', 'Return', 'Duration (sec.)', 'Covered distance (m)']

# Créer un nouveau DataFrame avec uniquement ces colonnes
Velomagg_filtree = Velomagg[columns]

Velomagg_final = Velomagg_filtree.dropna(subset=['Return station', 'Return'])

Velomagg_2023 = Velomagg_final[Velomagg_final['Departure'].astype(str).str.startswith('2023')]

# Charger les données
Velomagg_2023 = pd.read_csv("https://drive.google.com/uc?id=15tH6-xdxTAVr5KTnfPrxfQLObMyD9bew")

# Suppression des chiffres et des espaces devant les noms des stations
Velomagg_2023['Departure station'] = Velomagg_2023['Departure station'].str.replace(r'^\d+\s*', '', regex=True)
Velomagg_2023['Return station'] = Velomagg_2023['Return station'].str.replace(r'^\d+\s*', '', regex=True)

# Récupérer les noms uniques des stations de départ et de retour
departure_stations = Velomagg_2023['Departure station'].unique()
return_stations = Velomagg_2023['Return station'].unique()

# Combiner les deux listes pour obtenir tous les noms uniques
all_stations = pd.unique(pd.concat([pd.Series(departure_stations), pd.Series(return_stations)]))

# Créer un DataFrame à partir de la liste unique des stations
stations_df = pd.DataFrame(all_stations, columns=["Station Name"])

# Charger les fichiers CSV
df_velomagg = pd.read_csv("https://drive.google.com/uc?id=1VGH928Tt0TrrrJb2mIdHrybvLSCkziFi")
df_list = pd.read_csv("https://drive.google.com/uc?id=1seOdVZNyAnPaOo1Z82SvrTCNzxEkL-S_")

# Comparer les noms des stations
stations_with_coords = set(df_velomagg['nom'])
stations_list = set(df_list['Station Name'])

# Trouver les stations communes
stations_communes = stations_with_coords.intersection(stations_list)
print("Stations communes :")
print(stations_communes)

# Trouver les stations présentes uniquement dans stations_velomagg
stations_uniques_velomagg = stations_with_coords - stations_list
print("\nStations uniquement dans stations_with_coords.csv :")
print(stations_uniques_velomagg)

# Trouver les stations présentes uniquement dans stations_list
stations_uniques_list = stations_list - stations_with_coords
print("\nStations uniquement dans stations_list.csv :")
print(stations_uniques_list)