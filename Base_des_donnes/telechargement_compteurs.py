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

# %%