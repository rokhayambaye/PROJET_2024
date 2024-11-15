#%%
# my_data_package/downloader.py
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# Fonction pour trouver toutes les URLs des fichiers .json
def trouver_urls_json(url_base):
    response = requests.get(url_base)
    if response.status_code != 200:
        print(f"Échec de la récupération des donnees (Code {response.status_code})")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    liens = soup.find_all('a', href=True)  # Trouver tous les éléments <a> avec un attribut href
    urls_json = [urljoin(url_base, lien['href']) for lien in liens if lien['href'].endswith('.json')]
    
    return urls_json

# Fonction pour télécharger un fichier
def telecharger_fichier(url, dossier_destination):
    if "archive.json" in url: 
        response = requests.get(url)
        if response.status_code == 200:
            # Extraire le nom du fichier à partir de l'URL
            nom_fichier = url.split('/')[-1]
            chemin_complet = os.path.join(dossier_destination, nom_fichier)
        
            # Sauvegarder le fichier sur le disque
            with open(chemin_complet, 'wb') as fichier:
                fichier.write(response.content)
            print(f"Fichier téléchargé : {nom_fichier}")
        else:
             print(f"Échec du téléchargement du fichier {url} (Code {response.status_code})")

# URL de la page contenant les liens vers les fichiers JSON
url_base = "https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo"

# Dossier où les fichiers seront sauvegardés
dossier_destination = "donnees_montpellier"

# Créer le dossier de destination s'il n'existe pas
os.makedirs(dossier_destination, exist_ok=True)

# Récupérer les URLs des fichiers JSON
urls_json = trouver_urls_json(url_base)

# Télécharger les fichiers JSON
for url in urls_json:
    telecharger_fichier(url, dossier_destination)

# %%