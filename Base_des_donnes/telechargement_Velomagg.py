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

Velomagg = pd.read_csv(path_target)

# Colonnes souhaitées
columns =['Departure station', 'Departure', 'Return station', 'Return', 'Duration (sec.)', 'Covered distance (m)']

# Créer un nouveau DataFrame avec uniquement ces colonnes
Velomagg_filtree = Velomagg[columns]

Velomagg_final = Velomagg_filtree.dropna(subset=['Return station', 'Return'])

Velomagg_2023 = Velomagg_final[Velomagg_final['Departure'].astype(str).str.startswith('2023')]

# Créer un nouveau fichier CSV avec les données de Velomagg_2023
Velomagg_2023.to_csv("./Velomagg_2023.csv", index=False)

# %%
