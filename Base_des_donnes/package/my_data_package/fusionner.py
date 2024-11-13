# %%
import os
import json
import pandas as pd

def merge_json_files(output_dir="donnees_montpellier", output_file="donnees_ecocompteurs.csv"):
    """
    Fusionne les fichiers JSON présents dans un répertoire spécifié et crée un fichier CSV fusionné.

    Args:
        output_dir (str): Dossier contenant les fichiers JSON. Par défaut 'donnees_montpellier'.
        output_file (str): Nom du fichier de sortie fusionné. Par défaut 'donnees_ecocompteurs.csv'.
    """
    # Vérifier si le dossier de données existe
    if not os.path.exists(output_dir):
        print(f"Le répertoire spécifié '{output_dir}' n'existe pas.")
        return

    # Liste de tous les fichiers JSON dans le dossier
    json_files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
    if not json_files:
        print("Aucun fichier JSON trouvé à fusionner.")
        return

    # Initialiser une liste pour stocker les DataFrames
    dataframes = []

    # Charger et fusionner les fichiers JSON
    for file_name in json_files:
        file_path = os.path.join(output_dir, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Nettoyer les données si nécessaire (ex : remplacer les booléens non conformes)
                content = content.replace('False', 'false').replace('True', 'true')
                data = json.loads(content)
                df = pd.json_normalize(data)
                dataframes.append(df)
                print(f"Fichier {file_name} chargé avec succès.")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Erreur lors du chargement du fichier {file_name}: {e}. Le fichier sera ignoré.")

    # Concaténer tous les DataFrames
    if dataframes:
        merged_df = pd.concat(dataframes, ignore_index=True)
        # Enregistrer le DataFrame fusionné dans un fichier CSV
        merged_df.to_csv(output_file, index=False)
        print(f"Fusion réussie ! Les données ont été enregistrées dans '{output_file}'.")
    else:
        print("Aucune donnée valide à fusionner.")

