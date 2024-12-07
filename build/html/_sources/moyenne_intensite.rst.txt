.. _moyenne_intensite:

Traitement des Données de Compteurs
===================================

Le script suivant traite les données des éco-compteurs et calcule la moyenne de l'intensité du trafic pour chaque jour de la semaine. Il utilise des bibliothèques telles que `pandas` pour analyser les données.

Code source :
-------------

.. code-block:: python

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

Description du traitement :
---------------------------

1. **Chargement des données**  
   Le fichier CSV des éco-compteurs est téléchargé à partir de Google Drive et seules les colonnes nécessaires (`intensity`, `date`, `longitude`, `latitude`) sont extraites.

2. **Conversion de la date**  
   La colonne `date` est convertie en format `datetime` pour permettre l'extraction des informations temporelles, telles que le jour de la semaine.

3. **Extraction du jour de la semaine**  
   À l'aide de la méthode `dt.weekday`, le jour de la semaine est extrait de chaque ligne et converti en un nombre entier (0 pour lundi, 6 pour dimanche).

4. **Calcul des moyennes d'intensité**  
   La moyenne de l'intensité du trafic est calculée pour chaque combinaison de coordonnées (`longitude`, `latitude`) et jour de la semaine.

5. **Création du DataFrame final**  
   Les résultats obtenus (coordonnées, jour de la semaine, et intensité) sont stockés dans un nouveau DataFrame, prêt pour une analyse plus approfondie ou une visualisation.

Résultats :
-----------
Le DataFrame final (`df_resultats`) contient les informations suivantes :
- `longitude`: Longitude de la station.
- `latitude`: Latitude de la station.
- `jour`: Jour de la semaine.
- `intensite`: Moyenne de l'intensité du trafic pour ce jour de la semaine.
