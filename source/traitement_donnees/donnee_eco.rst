Gestionnaire de données éco (bike/Base_des_donnees/gestionnaire_donnee_eco)
===========================================================================

Ce module contient une classe et des méthodes pour télécharger, traiter et fusionner les données des éco-compteurs.

Description de la classe GestionnaireDonnees
--------------------------------------------
**GestionnaireDonnees** 

Cette classe permet de :  

- Télécharger les fichiers JSON des éco-compteurs.  

- Convertir les fichiers JSON en un format structuré.  

- Filtrer les données pour l'année 2023.  

- Fusionner les données des différents fichiers JSON dans un fichier CSV.    

- **Paramètres d'initialisation**

  - **url_base** : URL de base où les fichiers JSON sont disponibles.  
  - **dossier_brut** : Répertoire pour stocker les fichiers JSON téléchargés.  
  - **fichier_fusion** : Nom du fichier CSV final qui contiendra toutes les données fusionnées.  

- **Méthodes**

  - **telecharger_json()**  
      Télécharge les fichiers JSON disponibles à partir de l'URL de base.

  - **convertir_json_en_donnees(fichier_entree)**  
      Convertit les fichiers JSON en un DataFrame Pandas, avec filtrage des données invalides.

  - **fusionner_donnees()**  
      Fusionne les données filtrées de tous les fichiers JSON et les enregistre dans un fichier CSV.

  - **executer()**  
      Exécute l'intégralité du processus : téléchargement, conversion et fusion des données.

- **Exemple d'utilisation**

.. code-block:: python

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../bike/Base_des_donnees')))
    from gestionnaire_donnee_eco import GestionnaireDonnees

    # Définir les paramètres de gestion des données
    url_base = "https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo"
    dossier_brut = "dossier_json"
    fichier_fusion = "donnees_fusionnees.csv"

    # Créer une instance de la classe
    gestionnaire = GestionnaireDonnees(url_base, dossier_brut, fichier_fusion)

    # Exécuter le traitement complet
    gestionnaire.executer()

- **Fichier de sortie**

    - Le fichier CSV de sortie (**fichier_fusion**) contiendra les colonnes suivantes :
        - **intensity**, **laneId**, **date**, **longitude**, **latitude**, **id**, **type**, **vehicleType**, **reversedLane**
  
    - Seules les données de l'année 2023 seront incluses dans le fichier fusionné.

- **Notes supplémentaires**

    - Le processus de téléchargement est automatisé et inclut une validation des données pour garantir leur intégrité. 
     
    - Les données sont filtrées par date pour inclure uniquement celles de 2023.  
