#%%
import requests
from bs4 import BeautifulSoup
import os
import json
import pandas as pd
from urllib.parse import urljoin
import glob

class GestionnaireDonnees:
    def __init__(self, url_base, dossier_brut, dossier_nettoye, fichier_fusion):
        """
    Classe permettant de gérer le téléchargement, le traitement et la fusion des données des écocompteurs.

    Cette classe offre les fonctionnalités suivantes :
    1. Télécharger les fichiers JSON des écocompteurs à partir d'une URL de base.
    2. Traiter et nettoyer les fichiers JSON en les convertissant en CSV et en les filtrant pour l'année 2023.
    3. Fusionner tous les fichiers CSV nettoyés en un seul fichier CSV.

    Attributs :
    -----------
        url_base : str
        URL de la page contenant les liens vers les fichiers JSON.
        dossier_brut : str
            Dossier dans lequel les fichiers JSON seront téléchargés.
        dossier_nettoye : str
            Dossier où les fichiers CSV nettoyés seront enregistrés.
        fichier_fusion : str
            Chemin du fichier CSV fusionné à générer.

    Méthodes :
    ----------
        executer() :
            Exécute les trois étapes : téléchargement, traitement et fusion des fichiers.
    """

        self.url_base = url_base
        self.dossier_brut = dossier_brut
        self.dossier_nettoye = dossier_nettoye
        self.fichier_fusion = fichier_fusion

        os.makedirs(dossier_brut, exist_ok=True)
        os.makedirs(dossier_nettoye, exist_ok=True)

    def telecharger_json(self):
        """
        Télécharge tous les fichiers JSON disponibles à l'URL de base.
        """
        print("Recherche des fichiers JSON à télécharger...")
        response = requests.get(self.url_base)
        if response.status_code != 200:
            print(f"Échec de la récupération des données (Code {response.status_code})")
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        liens = soup.find_all('a', href=True)
        urls_json = [urljoin(self.url_base, lien['href']) for lien in liens if lien['href'].endswith('.json')]

        for url in urls_json:
            if "archive.json" in url: 
                response = requests.get(url)
                if response.status_code == 200:
                    nom_fichier = os.path.basename(url)
                    chemin_complet = os.path.join(self.dossier_brut, nom_fichier)
                    with open(chemin_complet, 'wb') as fichier:
                        fichier.write(response.content)
                    print(f"Fichier téléchargé : {nom_fichier}")
                else:
                    print(f"Échec du téléchargement du fichier {url} (Code {response.status_code})")

    def convertir_json_en_csv(self, fichier_entree):
        """
        Convertit un fichier JSON en fichier CSV nettoyé.
        :param fichier_entree: Chemin du fichier JSON d'entrée.
        :return: True si la conversion a réussi, False sinon.
        """
        nom_fichier_entree = os.path.basename(fichier_entree)
        nom_fichier_sortie = nom_fichier_entree.replace('.json', '.csv')
        fichier_sortie = os.path.join(self.dossier_nettoye, nom_fichier_sortie)

        liste_donnees = []
        try:
            with open(fichier_entree, 'r', encoding='utf-8') as fichier:
                for ligne in fichier:
                    ligne = ligne.strip()
                    if not ligne:
                        continue
                    chaines_json = ligne.replace('}{', '}\n{').split('\n')
                    for chaine_json in chaines_json:
                        try:
                            objet_json = json.loads(chaine_json)
                            if any(objet_json.get(cle) is None for cle in [
                                'intensity', 'laneId', 'dateObserved', 'location', 'id', 'type', 'vehicleType', 'reversedLane']):
                                continue
                            if objet_json['location'].get('coordinates') is None or None in objet_json['location']['coordinates']:
                                continue
                            date = objet_json['dateObserved'].split('T')[0]
                            donnees_aplatis = {
                                'intensity': objet_json['intensity'],
                                'laneId': objet_json['laneId'],
                                'date': date,
                                'longitude': objet_json['location']['coordinates'][0],
                                'latitude': objet_json['location']['coordinates'][1],
                                'id': objet_json['id'],
                                'type': objet_json['type'],
                                'vehicleType': objet_json['vehicleType'],
                                'reversedLane': objet_json['reversedLane']
                            }
                            liste_donnees.append(donnees_aplatis)
                        except (json.JSONDecodeError, KeyError):
                            continue

            if not liste_donnees:
                print(f"Aucune donnée valide trouvée dans {nom_fichier_entree}.")
                return False

            df = pd.DataFrame(liste_donnees).dropna()
            df['date'] = pd.to_datetime(df['date'])
            masque = (df['date'] >= '2023-01-01') & (df['date'] <= '2023-12-31')
            df_filtré = df.loc[masque].sort_values('date')
            df_filtré['date'] = df_filtré['date'].dt.strftime('%Y-%m-%d')

            if not df_filtré.empty:
                df_filtré.to_csv(
                    fichier_sortie, 
                    index=False, 
                    sep=';', 
                    encoding='utf-8-sig', 
                    float_format='%.6f')
                print(f"Conversion réussie : {nom_fichier_entree} -> {nom_fichier_sortie}")
                return True
            else:
                print(f"Aucune donnée pertinente dans {nom_fichier_entree}.")
                return False
        except Exception as e:
            print(f"Erreur lors de la conversion de {nom_fichier_entree} : {str(e)}")
            return False

    def traiter_fichiers_json(self):
        """
        Traite tous les fichiers JSON du dossier brut.
        """
        json_files = glob.glob(os.path.join(self.dossier_brut, '*.json'))
        if not json_files:
            print("Aucun fichier JSON à traiter.")
            return

        print(f"Fichiers JSON trouvés : {len(json_files)}")
        for fichier in json_files:
            self.convertir_json_en_csv(fichier)

    def fusionner_csv(self):
        """
        Fusionne tous les fichiers CSV nettoyés dans un seul fichier CSV.
        """
        data_frames = []
        for file_name in os.listdir(self.dossier_nettoye):
            if file_name.endswith('.csv'):
                file_path = os.path.join(self.dossier_nettoye, file_name)
                df = pd.read_csv(file_path)
                data_frames.append(df)
                print(f"Fichier ajouté pour fusion : {file_name}")
        
        if data_frames:
            merged_df = pd.concat(data_frames, ignore_index=True)
            merged_df.to_csv(self.fichier_fusion, index=False)
            print(f"Fichier fusionné enregistré sous : {self.fichier_fusion}")
        else:
            print("Aucun fichier CSV disponible pour fusion.")

    def executer(self):
        """
        Exécute tout le pipeline : téléchargement, traitement et fusion.
        """
        self.telecharger_json()
        self.traiter_fichiers_json()
        self.fusionner_csv()


# Exemple d'utilisation
url_base = "https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo"
dossier_brut = "Base_des_donnees/donnees_montpellier"
dossier_nettoye = "Base_des_donnees/donnees_montpellier_2023_nettoyer"
fichier_fusion = "Base_des_donnees/donnees_montpellier_2023.csv"

gestionnaire = GestionnaireDonnees(url_base, dossier_brut, dossier_nettoye, fichier_fusion)
gestionnaire.executer()

# %%
