#%%
import os
import pandas as pd
import seaborn as sns 
import pooch

#%%
sns.set_palette("colorblind")
palette = sns.color_palette("twilight", n_colors=12)
pd.options.display.max_rows = 8
# Définir l'URL
url = 'https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_GeolocCompteurs.csv'
path_target = "./MMM_MMM_GeolocCompteurs.csv"
path, fname = os.path.split(path_target)
pooch.retrieve(url, path=path, fname=fname, known_hash=None)  
MMM_MMM_GeolocCompteurs = pd.read_csv("MMM_MMM_GeolocCompteurs.csv")
MMM_MMM_GeolocCompteurs.info()
MMM_MMM_GeolocCompteurs.head(n=100)
# Colonnes souhaitées

# Créer un nouveau DataFrame avec uniquement ces colonnes
# Extraire uniquement les colonnes 'Latitude' et 'Longitude'
MMM_MMM_GeolocCompteurs_final = MMM_MMM_GeolocCompteurs[['Latitude', 'Longitude','OSM_Line_i']]

# Afficher les premières lignes du DataFrame filtré
MMM_MMM_GeolocCompteurs_final.head(100)

# %%
