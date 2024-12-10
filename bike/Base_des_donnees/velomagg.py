
import pandas as pd

class TraitementDonneesVelomagg:
    """
    Classe permettant  de traiter et nettoyer des données de trajets de vélos , 
    en ajoutant les coordonnées des stations de départ et de retour, et en enregistrant 
    dans un fichier CSV.

    Paramètres
    ----------
    url_trajets : str
        url du fichier csv contenant les données des trajets des vélos velomagg de l année 2023.
    url_stations : str
        url du fichier CSV contenant les données des stations.
    fichier_sortie : str
        Nom du fichier CSV où les données enrichies seront sauvegardées.
    df_trajets : pandas.DataFrame, optionnel
        DataFrame contenant les données des trajets après traitement.
    dict_stations : dict, optionnel
        Dictionnaire contenant les coordonnées (latitude et longitude) des stations.

    Méthodes
    --------
    telecharger_et_nettoyer_trajets()
        Télécharge et nettoie les données des trajets, corrige les noms des stations.
    ajouter_coordonnees_stations()
        télécharge les données des stations et ajoute les coordonnées aux trajets.
    supprimer_lignes_manquantes()
        supprime les lignes contenant des  valeurs manquantes dans les données des trajets des velos.
    sauvegarder_csv()
        enregistre les données dans un fichier CSV.
    executer()
        exécute l'ensemble du processus de traitement des données.
    """
    
    def __init__(self, url_trajets, url_stations, fichier_sortie="Velomagg_avec_coordonnees.csv"):
        # Initialisation des URLs et du fichier de sortie
        self.url_trajets = url_trajets
        self.url_stations = url_stations
        self.fichier_sortie = fichier_sortie
        self.df_trajets = None
        self.dict_stations = None

    def telecharger_et_nettoyer_trajets(self):
        # Téléchargement des données de trajets
        print("Téléchargement et nettoyage des donnees de trajets...")
        self.df_trajets = pd.read_csv(self.url_trajets)

        # Remplacements pour nettoyer les noms des stations
        remplacements = {
            'Ã©': 'é', 'Ã¨': 'è', 'Ã´': 'ô',
            r'^\d+\s*': '', 'Antigone centre': 'Antigone Centre',
            'Fac de Lettres': 'Fac des Sciences', 'Perols etang or': 'Pérols',
            "Pérols Etang de l'Or": 'Pérols', 'Sud De France': 'Montpellier Sud de France',
            'Albert 1er - Cathédrale': 'Albert 1er - Cathedrale',
            'Place Albert 1er - St Charles': 'Place Albert 1er - St-Charles',
            'Pont de Lattes - Gare Saint-Roch': 'Pont de Lattes - Gare St-Roch',
            'Rue Jules Ferry - Gare Saint-Roch': 'Rue Jules Ferry',
            'Parvis Jules Ferry - Gare Saint-Roch': 'Parvis Jules Ferry',
            "Prés d'Arènes": "Près d'Arènes", "Providence - Ovalie": "Providence-Ovalie",
            'FacdesSciences': 'Fac des Sciences', 'Clemenceau': 'Clémenceau'
        }
        # Appliquer les remplacements aux colonnes 'Departure station' et 'Return station'
        for ancien, nouveau in remplacements.items():
            self.df_trajets['Departure station'] = self.df_trajets['Departure station'].str.replace(ancien, nouveau, regex=True)
            self.df_trajets['Return station'] = self.df_trajets['Return station'].str.replace(ancien, nouveau, regex=True)

        # Sélection des colonnes nécessaires et suppression des lignes avec des valeurs manquantes
        colonnes = ['Departure station', 'Departure', 'Return station', 'Return', 'Duration (sec.)', 'Covered distance (m)']
        self.df_trajets = self.df_trajets[colonnes].dropna(subset=['Return station', 'Return'])
        print("Nettoyage termine.")

    def ajouter_coordonnees_stations(self):
        # Téléchargement des données des stations
        print("Téléchargement des donnees des stations...")
        df_stations = pd.read_csv(self.url_stations)
        # Création d'un dictionnaire des coordonnées des stations
        self.dict_stations = df_stations.set_index('nom')[['latitude', 'longitude']].to_dict(orient='index')

        # Fonction pour récupérer les coordonnées d'une station donnée
        def obtenir_lat_lon(nom_station):
            if nom_station in self.dict_stations:
                return self.dict_stations[nom_station]['latitude'], self.dict_stations[nom_station]['longitude']
            else:
                return None, None

        # Ajout des coordonnées aux stations de départ et d'arrivée
        print("Ajout des coordonnees aux trajets...")
        self.df_trajets['latitude_depart'], self.df_trajets['longitude_depart'] = zip(*self.df_trajets['Departure station'].apply(obtenir_lat_lon))
        self.df_trajets['latitude_retour'], self.df_trajets['longitude_retour'] = zip(*self.df_trajets['Return station'].apply(obtenir_lat_lon))

    def supprimer_lignes_manquantes(self):
        # Suppression des lignes avec des données manquantes
        print("Suppression des lignes contenant des donnees manquantes...")
        nombre_initial = len(self.df_trajets)
        self.df_trajets = self.df_trajets.dropna()
        nombre_final = len(self.df_trajets)
        print(f"{nombre_initial - nombre_final} lignes supprimees. {nombre_final} lignes restantes.")

    def sauvegarder_csv(self):
        # Enregistrement des données enrichies dans un fichier CSV
        print(f"Enregistrement des donnees enrichies dans {self.fichier_sortie}...")
        self.df_trajets.to_csv(self.fichier_sortie, index=False)
        print("Enregistrement termine.")

    def executer(self):
        # Exécution de toutes les étapes du traitement
        self.telecharger_et_nettoyer_trajets()
        self.ajouter_coordonnees_stations()
        self.supprimer_lignes_manquantes()
        self.sauvegarder_csv()
