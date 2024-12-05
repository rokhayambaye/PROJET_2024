#%%
import pandas as pd
import seaborn as sns 

sns.set_palette("colorblind")
palette = sns.color_palette("twilight", n_colors=12)
pd.options.display.max_rows = 8
Velomagg = pd.read_csv('https://drive.google.com/uc?id=1kUMForLXwdGvV9ha2Qx-vMd6CnoMnWV5')
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
#changer les noms de quelques stations pour pouvoir recuperer leur coordonnées
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
Velomagg['Departure station'] =Velomagg['Departure station'].str.replace('FacdesSciences', 'Fac des Sciences')
Velomagg['Return station'] =Velomagg['Return station'].str.replace('FacdesSciences',  'Fac des Sciences')
Velomagg['Departure station'] =Velomagg['Departure station'].str.replace('Clemenceau', 'Clémenceau')
Velomagg['Return station'] =Velomagg['Return station'].str.replace('Clemenceau',  'Clémenceau')
# Colonnes souhaitées
columns =['Departure station', 'Departure', 'Return station', 'Return', 'Duration (sec.)', 'Covered distance (m)']

# Créer un nouveau DataFrame avec uniquement ces colonnes
Velomagg= Velomagg[columns]

Velomagg= Velomagg.dropna(subset=['Return station', 'Return'])
Velomagg.to_csv('Velomagg.csv', index=False)
