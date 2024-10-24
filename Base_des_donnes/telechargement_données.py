#%%
import os
import pandas as pd
import seaborn as sns 
import pooch

sns.set_palette("colorblind")
palette = sns.color_palette("twilight", n_colors=12)
pd.options.display.max_rows = 8

url ="https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_CoursesVelomagg.csv"
path_target = "./CoursesVelomagg.csv"
path, fname = os.path.split(path_target)
pooch.retrieve(url, path=path, fname=fname, known_hash=None)

Velomagg = pd.read_csv("CoursesVelomagg.csv")

Velomagg.info()
# %%
import requests
import json

# Définir l'URL
url = 'https://portail-api-data.montpellier3m.fr/ecocounter_timeseries/urn:ngsi-ld:EcoCounter:X2H19070220/attrs/intensity?fromDate=2022-10-01T00:00:00&toDate=2023-10-01T00:00:00'

# Faire une requête GET à l'API
response = requests.get(url, headers={'accept': 'application/json'})

# Vérifier le statut de la réponse
if response.status_code == 200:
    # Traiter les données JSON
    data = response.json()
    # Enregistrer les données dans un fichier JSON
    with open('donnees_ecocounter.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Données téléchargées avec succès.")
else:
    print(f"Erreur : {response.status_code} - {response.text}")
path, fname = os.path.split(path_target)
pooch.retrieve(url, path=path, fname=fname, known_hash=None)
path_target = "./Compteurs.json"
path, fname = os.path.split(path_target)
pooch.retrieve(url, path=path, fname=fname, known_hash=None)  
# %%
compteurs = pd.read_json("Compteurs.json")
compteurs.info()
compteurs.head()


# %%
