import json
import pandas as pd
import os
import glob

# Conversion et sélection des données 

def convertir_json_en_csv(input_file, output_dir):
    # Créer le nom du fichier de sortie dans le dossier data_clean
    nom_fichier_entree = os.path.basename(input_file)
    nom_fichier_sortie = nom_fichier_entree.replace('.json', '.csv')
    fichier_sortie = os.path.join(output_dir, nom_fichier_sortie)
    
    # Lire le fichier et stocker les données
    liste_donnees = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as fichier:
            # Lire le fichier ligne par ligne
            for ligne in fichier:
                # Ignorer les lignes vides
                ligne = ligne.strip()
                if not ligne:
                    continue
                    
                # Séparer les objets JSON qui pourraient être collés ensemble
                chaines_json = ligne.replace('}{', '}\n{').split('\n')
                
                for chaine_json in chaines_json:
                    try:
                        if not chaine_json.strip():
                            continue
                        # Charger l'objet JSON   
                        objet_json = json.loads(chaine_json)
                        
                        # Vérifier si des valeurs importantes sont nulles
                        if any(objet_json.get(cle) is None for cle in ['intensity', 'laneId', 'dateObserved', 'location', 'id', 'type', 'vehicleType', 'reversedLane']):
                            continue
                            
                        # Vérifier si les coordonnées sont nulles
                        if objet_json['location'].get('coordinates') is None or None in objet_json['location']['coordinates']:
                            continue
                        
                        # Extraire la date
                        date = objet_json['dateObserved'].split('T')[0]
                        
                        # Créer un dictionnaire aplati
                        donnees_aplatis = {
                            'intensity': objet_json['intensity'],
                            'laneId': objet_json['laneId'],
                            'date': date,
                            # Extraire les coordonnées
                            'longitude': objet_json['location']['coordinates'][0],
                            'latitude': objet_json['location']['coordinates'][1],
                            'id': objet_json['id'],
                            'type': objet_json['type'],
                            'vehicleType': objet_json['vehicleType'],
                            'reversedLane': objet_json['reversedLane']
                        }
                        
                        # Vérifier si une des valeurs du dictionnaire est nulle
                        if any(valeur is None for valeur in donnees_aplatis.values()):
                            continue
                        
                        liste_donnees.append(donnees_aplatis)
                    except json.JSONDecodeError as e:
                        print(f"Erreur de décodage JSON : {str(e)}\nDans l'objet : {chaine_json[:50]}...")
                        continue
                    except KeyError as e:
                        print(f"Clé manquante dans l'objet : {str(e)}")
                        continue
        # Si aucune donnée n'a été trouvée, lever une exception
        if not liste_donnees:
            raise ValueError("Aucune donnée valide trouvée dans le fichier")
        
        # Convertir en DataFrame pandas
        df = pd.DataFrame(liste_donnees)
        
        # Si le DataFrame est vide, stopper et retourner False
        if df.empty:
            print(f"Aucune donnée à sauvegarder pour {nom_fichier_entree}. Le fichier ne sera pas créé.")
            return False
        
        # Supprimer les lignes contenant des valeurs nulles
        df = df.dropna()
        
        # Convertir la colonne de date en format datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Filtrer les données pour l'année 2023
        masque = (df['date'] >= '2023-01-01') & (df['date'] <= '2023-12-31')
        df_filtre = df.loc[masque]
        
        # Trier par date
        df_filtre = df_filtre.sort_values('date')
        
        # Convertir la date en format string YYYY-MM-DD pour le CSV
        df_filtre['date'] = df_filtre['date'].dt.strftime('%Y-%m-%d')
        
        # Sauvegarder en CSV avec des paramètres explicites
        df_filtre.to_csv(fichier_sortie, 
                          index=False,
                          sep=';',
                          encoding='utf-8-sig',
                          float_format='%.6f')
        
        # Afficher le message de succès avant de retourner
        print(f"\nConversion réussie : {nom_fichier_entree} -> {nom_fichier_sortie}")
        print(f"Nombre total d'enregistrements : {len(liste_donnees)}")
        print(f"Nombre d'enregistrements dans la période : {len(df_filtre)}")
        if not df_filtre.empty:
            print(f"Période : du {df_filtre['date'].min()} au {df_filtre['date'].max()}")
        
        # Indiquer le succès de la conversion
        return True if not df_filtre.empty else False
        
    except Exception as e:
        print(f"\nErreur lors du traitement de {nom_fichier_entree}")
        print(f"Erreur : {str(e)}")
        return False

def process_all_json_files():
    # Définir les chemins d'accès aux dossiers
    input_dir = 'bike/Base_des_donnees/donnees_montpellier'  
    output_dir = 'bike/Base_des_donnees/donnees_montpellier_2023_nettoyer' 

    # Vérifier si le dossier d'entrée existe
    if not os.path.exists(input_dir):
        print(f"Erreur : le dossier 'donnees_montpellier' n'existe pas à {input_dir}")
        return

    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Dossier 'donnees_montpellier_nettoyer' créé à {output_dir}")

    # Rechercher tous les fichiers .json dans le dossier d'entrée
    json_files = glob.glob(os.path.join(input_dir, '*.json'))

    if not json_files:
        print("Aucun fichier .json trouvé dans le dossier 'donnees_montpellier'.")
        return

    print(f"Nombre de fichiers .json trouvés : {len(json_files)}")

    # Comptage des succès et des erreurs
    success_count = 0
    error_count = 0

    # Traiter chaque fichier
    for json_file in json_files:
        print(f"\nTraitement de : {os.path.basename(json_file)}")
        # Convertir le fichier et vérifier si la conversion a échoué
        if not convertir_json_en_csv(json_file, output_dir):
            output_filename = os.path.basename(json_file).replace('.json', '.csv')
            output_file = os.path.join(output_dir, output_filename)
            if os.path.exists(output_file):
                os.remove(output_file)  # Supprimer le fichier CSV si la conversion a échoué
                print(f"{output_filename} supprimé car vide.")
            error_count += 1
        else:
            success_count += 1

    # Rapport final
    print("\n=== Rapport de conversion ===")
    print(f"Fichiers traités avec succès : {success_count}")
    print(f"Fichiers sans enregistrement pour la période souhaitée : {error_count}")
    print(f"Total de fichiers : {len(json_files)}")
    print(f"\nLes fichiers CSV ont été enregistrés dans : {output_dir}")

# Lancer le traitement
process_all_json_files()