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
