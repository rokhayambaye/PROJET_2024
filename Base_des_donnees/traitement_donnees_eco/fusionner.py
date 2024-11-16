# %%
import os
import json
import pandas as pd
import os
import pandas as pd

def merge_csv_files(folder_path, output_file):
    # Liste pour stocker tous les DataFrames
    data_frames = []
    
    # Parcourt chaque fichier CSV dans le dossier spécifié
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            # Lire le fichier CSV et l'ajouter à la liste
            df = pd.read_csv(file_path)
            data_frames.append(df)
            print(f"Fichier ajouté pour fusion : {file_name}")
    
    # Combine tous les DataFrames dans un seul
    merged_df = pd.concat(data_frames, ignore_index=True)
    
    # Enregistrer le DataFrame fusionné dans un nouveau fichier CSV
    merged_df.to_csv(output_file, index=False)
    print(f"Fichier fusionné enregistré sous : {output_file}")

# Spécifiez le dossier contenant les fichiers filtrés et le fichier de sortie fusionné
folder_path = 'Base_des_donnees/donnees_montpellier_2023_nettoyer'
output_file = 'Base_des_donnees/donnees_montpellier_2023.csv'







# %%
merge_csv_files(folder_path, output_file)
# %%
