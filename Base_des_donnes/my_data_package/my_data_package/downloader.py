#%%
# my_data_package/downloader.py
import subprocess
import os
import pandas as pd
import seaborn as sns 
import pooch
def download_data( output_dir, from_date, to_date):
    # Lire le fichier CSV avec pandas
    sns.set_palette("colorblind")
    palette = sns.color_palette("twilight", n_colors=12)
    pd.options.display.max_rows = 8
    # Définir l'URL
    url = 'https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_GeolocCompteurs.csv'
    path_target = "./MMM_MMM_GeolocCompteurs.csv"
    path, fname = os.path.split(path_target)
    pooch.retrieve(url, path=path, fname=fname, known_hash=None)  
    df = pd.read_csv("MMM_MMM_GeolocCompteurs.csv")
    #Recuperer le nom des compteurs 
    compteurs = df['N° Série'].tolist()
    os.makedirs(output_dir, exist_ok=True)

    # URL de base de l'API
    base_url = "https://portail-api-data.montpellier3m.fr/ecocounter_timeseries"

    # Télécharger les données pour chaque compteur
    for compteur in compteurs:
        url = f"{base_url}/{compteur}/attrs/intensity?fromDate={from_date}&toDate={to_date}"

        # Nom du fichier basé sur le numero de serie du compteur
        file_name = f"{compteur.split(':')[-1]}.json"
        file_path = os.path.join(output_dir, file_name)

        # Exécution de la commande cURL pour télécharger les données
        try:
            subprocess.run(["curl", "-o", file_path, url], check=True)
            print(f"Les données pour {compteur} ont été téléchargées dans {file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors du téléchargement des données pour {compteur}: {e}")
#%%
import subprocess
import os
import pandas as pd
import pooch

def download_dataarchive(output_dir="data_compteurs"):
    # Lire le fichier CSV contenant la liste des compteurs
    url_csv = 'https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_GeolocCompteurs.csv'
    path_target_csv = "./MMM_MMM_GeolocCompteurs.csv"
    path, fname_csv = os.path.split(path_target_csv)

    # Utiliser pooch pour télécharger le fichier CSV
    pooch.retrieve(url_csv, path=path, fname=fname_csv, known_hash=None)  
    df = pd.read_csv(path_target_csv)

    # Récupérer le nom des compteurs (en supposant que la colonne "N° Série" contient les ID des compteurs)
    compteurs = df['N° Série'].tolist()

    # Créer un répertoire de sortie pour les données
    os.makedirs(output_dir, exist_ok=True)

    # URL de base pour les archives JSON des compteurs
    archive_base_url = "https://data.montpellier3m.fr/sites/default/files/ressources/"

    # Télécharger les archives JSON pour chaque compteur
    for compteur in compteurs:
        # Construire le nom du fichier d'archive basé sur le numéro de série du compteur
        file_name = f"MMM_EcoCompt_{compteur.split(':')[-1]}_archive.json"
        file_url = f"{archive_base_url}{file_name}"

        # Chemin de destination pour le fichier JSON
        file_path_json = os.path.join(output_dir, file_name)

        # Exécution de la commande cURL pour télécharger l'archive JSON
        try:
            subprocess.run(["curl", "-o", file_path_json, file_url], check=True)
            print(f"Les données pour {compteur} ont été téléchargées dans {file_path_json}")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors du téléchargement des données pour {compteur}: {e}")

# %%
