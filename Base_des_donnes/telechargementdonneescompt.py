
# %%
import subprocess
import os
import pandas as pd

# Lire le fichier CSV avec pandas
csv_file = '/Users/rokhayambaye/HAX712X/PROJET_2024/Base_des_donnes/MMM_MMM_GeolocCompteurs.csv' 
df = pd.read_csv(csv_file)
compteurs = df['N° Série'].tolist()
output_dir = "data_compteurs"
os.makedirs(output_dir, exist_ok=True)
from_date = "2023-01-01T00:00:00"
to_date = "2023-12-31T23:59:59"
# URL de base de l'API
base_url = "https://portail-api-data.montpellier3m.fr/ecocounter_timeseries"

# Télécharger les données pour chaque compteur
for compteur in compteurs:
    url = f"{base_url}/{compteur}/attrs/intensity?fromDate={from_date}&toDate={to_date}"

    # Nom du fichier basé sur l'ID du compteur
    file_name = f"{compteur.split(':')[-1]}.json"
    file_path = os.path.join(output_dir, file_name)

    # Exécution de la commande cURL pour télécharger les données
    try:
        subprocess.run(["curl", "-o", file_path, url], check=True)
        print(f"Les données pour {compteur} ont été téléchargées dans {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du téléchargement des données pour {compteur}: {e}")


# %%
