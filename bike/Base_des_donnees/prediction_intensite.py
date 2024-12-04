import pandas as pd

compteurs_df = pd.read_csv("https://drive.google.com/uc?id=1yJUkkGiobznF50tQaKwbM4a2bfiEVmRy", delimiter=';')
compteurs_df = compteurs_df[['intensity','date','longitude','latitude']]

# S'assurer que la colonne 'date' est bien en format datetime
compteurs_df['date'] = pd.to_datetime(compteurs_df['date'], format='%Y-%m-%d')

# Extraire le jour de la semaine (lundi=0, mardi=1, ..., dimanche=6)
compteurs_df['jour_semaine'] = compteurs_df['date'].dt.weekday

# Moyenne de l'intensité pour id et jour
moyennes_intensite = compteurs_df.groupby(['longitude', 'latitude','jour_semaine'])['intensity'].mean().reset_index()

day = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

resultats = []
for idx, row in moyennes_intensite.iterrows():
    jour = int(row['jour_semaine'])
    intensite = row['intensity']
    longitude = row['longitude']
    latitude = row['latitude']
    resultats.append([longitude, latitude, day[jour], intensite])

# Convertir les résultats en DataFrame
df_resultats = pd.DataFrame(resultats, columns=['longitude','latitude', 'jour', 'intensite'])