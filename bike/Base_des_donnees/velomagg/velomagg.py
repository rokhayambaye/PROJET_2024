#%%
import pandas as pd

class TraitementDonneesVelomagg:
    def __init__(self, url_trajets, url_stations, fichier_sortie="Velomagg_avec_coordonnees.csv"):
        """
        Initialise le traitement des données Velomagg.
        
        :param url_trajets: URL du fichier CSV contenant les trajets.
        :param url_stations: URL du fichier CSV contenant les stations et leurs coordonnées.
        :param fichier_sortie: Nom du fichier de sortie contenant les données enrichies.
        """
        self.url_trajets = url_trajets
        self.url_stations = url_stations
        self.fichier_sortie = fichier_sortie
        self.df_trajets = None
        self.dict_stations = None

    def telecharger_et_nettoyer_trajets(self):
        """Télécharge et nettoie les données de trajets."""
        print("Téléchargement et nettoyage des données de trajets...")
        self.df_trajets = pd.read_csv(self.url_trajets)

        # Nettoyage des noms de stations
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
        for ancien, nouveau in remplacements.items():
            self.df_trajets['Departure station'] = self.df_trajets['Departure station'].str.replace(ancien, nouveau, regex=True)
            self.df_trajets['Return station'] = self.df_trajets['Return station'].str.replace(ancien, nouveau, regex=True)

        # Sélectionner les colonnes nécessaires et supprimer les lignes avec des valeurs manquantes
        colonnes = ['Departure station', 'Departure', 'Return station', 'Return', 'Duration (sec.)', 'Covered distance (m)']
        self.df_trajets = self.df_trajets[colonnes].dropna(subset=['Return station', 'Return'])
        
        print("Nettoyage terminé.")

    def ajouter_coordonnees_stations(self):
        """Ajoute les coordonnées des stations de départ et d'arrivée aux données de trajets."""
        print("Téléchargement des données des stations...")
        df_stations = pd.read_csv(self.url_stations)
        self.dict_stations = df_stations.set_index('nom')[['latitude', 'longitude']].to_dict(orient='index')

        def obtenir_lat_lon(nom_station):
            if nom_station in self.dict_stations:
                return self.dict_stations[nom_station]['latitude'], self.dict_stations[nom_station]['longitude']
            else:
                return None, None

        print("Ajout des coordonnées aux trajets...")
        self.df_trajets['latitude_depart'], self.df_trajets['longitude_depart'] = zip(*self.df_trajets['Departure station'].apply(obtenir_lat_lon))
        self.df_trajets['latitude_retour'], self.df_trajets['longitude_retour'] = zip(*self.df_trajets['Return station'].apply(obtenir_lat_lon))

    def supprimer_lignes_manquantes(self):
        """Supprime les lignes contenant des valeurs manquantes dans le DataFrame."""
        print("Suppression des lignes contenant des données manquantes...")
        nombre_initial = len(self.df_trajets)
        self.df_trajets = self.df_trajets.dropna()
        nombre_final = len(self.df_trajets)
        print(f"{nombre_initial - nombre_final} lignes supprimées. {nombre_final} lignes restantes.")

    def sauvegarder_csv(self):
        """Enregistre le DataFrame enrichi dans un fichier CSV."""
        print(f"Enregistrement des données enrichies dans {self.fichier_sortie}...")
        self.df_trajets.to_csv(self.fichier_sortie, index=False)
        print("Enregistrement terminé.")

    def executer(self):
        """Exécute l'ensemble du processus : téléchargement, nettoyage, ajout des coordonnées et sauvegarde."""
        self.telecharger_et_nettoyer_trajets()
        self.ajouter_coordonnees_stations()
        self.supprimer_lignes_manquantes()
        self.sauvegarder_csv()

# %%
# Définir les URL des fichiers
url_trajets = "https://drive.google.com/uc?id=1kUMForLXwdGvV9ha2Qx-vMd6CnoMnWV5"
url_stations = "https://drive.google.com/uc?id=1HgOLf2JD46ZJlyrF_c99QZb6of6ajNYh"

# Créer une instance de la classe et traiter les données
traitement = TraitementDonneesVelomagg(url_trajets, url_stations)
traitement.executer()

# %%
