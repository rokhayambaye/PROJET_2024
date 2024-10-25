#%%
import os
import pandas as pd
import seaborn as sns 
import pooch

sns.set_palette("colorblind")
palette = sns.color_palette("twilight", n_colors=12)
pd.options.display.max_rows = 8
# Définir l'URL
url = 'https://portail-api-data.montpellier3m.fr/ecocounter_timeseries/urn:ngsi-ld:EcoCounter:X2H19070220/attrs/intensity?fromDate=2022-10-01T00:00:00&toDate=2023-10-01T00:00:00'
path, fname = os.path.split(path_target)
pooch.retrieve(url, path=path, fname=fname, known_hash=None)
path_target = "./Compteurs.json"
path, fname = os.path.split(path_target)
pooch.retrieve(url, path=path, fname=fname, known_hash=None)  
compteurs = pd.read_json("Compteurs.json")
compteurs.info()
compteurs.head()

