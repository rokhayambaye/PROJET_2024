
# %% Importation des modules nécessaires
import sys
import os

# Ajoute le répertoire parent du dossier 'bike' au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bike', 'Base_des_donnees')))

# Importation de la classe
from velomagg import TraitementDonneesVelomagg

def tester_traitement_donnees_velomagg():
    # URLs des données
    url_trajets = "https://drive.google.com/uc?id=1kUMForLXwdGvV9ha2Qx-vMd6CnoMnWV5"
    url_stations = "https://drive.google.com/uc?id=1HgOLf2JD46ZJlyrF_c99QZb6of6ajNYh"
    
    # Fichier de sortie pour les tests
    fichier_sortie_test = os.path.abspath("test_Velomagg_avec_coordonnees.csv")
    
    # Créer une instance de la classe avec un fichier de sortie défini
    traitement = TraitementDonneesVelomagg(url_trajets, url_stations)
    traitement.fichier_sortie = fichier_sortie_test  # Rediriger le fichier de sortie
    
    # Vérifier ou créer le dossier de sortie
    dossier_sortie = os.path.dirname(traitement.fichier_sortie)
    if dossier_sortie and not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)
        print(f"Dossier de sortie créé : {dossier_sortie}")
    
    # Test de la méthode de téléchargement et nettoyage des trajets
    print("Test: Téléchargement et nettoyage des trajets")
    traitement.telecharger_et_nettoyer_trajets()
    assert traitement.df_trajets is not None, "Les trajets n'ont pas été téléchargés correctement"
    assert 'Departure station' in traitement.df_trajets.columns, "La colonne 'Departure station' est manquante"
    print("Téléchargement et nettoyage des trajets réussis")

    # Test de la méthode d'ajout des coordonnées
    print("Test: Ajout des coordonnées des stations")
    traitement.ajouter_coordonnees_stations()
    assert 'latitude_depart' in traitement.df_trajets.columns, "La colonne 'latitude_depart' est manquante"
    assert 'longitude_depart' in traitement.df_trajets.columns, "La colonne 'longitude_depart' est manquante"
    print("Ajout des coordonnées réussi")

    # Test de la méthode de suppression des lignes manquantes
    print("Test: Suppression des lignes manquantes")
    traitement.supprimer_lignes_manquantes()
    assert not traitement.df_trajets.isnull().values.any(), "Des valeurs manquantes subsistent"
    print("Suppression des lignes manquantes réussie")
    
# Appeler la fonction de test
tester_traitement_donnees_velomagg()
# %%
