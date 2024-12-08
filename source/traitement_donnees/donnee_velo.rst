Traitement des Données VéloMagg
================================

Ce module contient une classe et des méthodes pour télécharger, nettoyer et enrichir les données des trajets VéloMagg avec les coordonnées des stations.

Classe principale
------------------

**TraitementDonneesVelomagg**

Cette classe permet de :
1. Télécharger les données de trajets et des stations.
2. Nettoyer les noms des stations.
3. Ajouter les coordonnées (latitude et longitude) aux stations de départ et d'arrivée des trajets.
4. Supprimer les lignes avec des valeurs manquantes.
5. Sauvegarder les données traitées dans un fichier CSV.

### Paramètres d'initialisation

- **url_trajets** : URL contenant les données des trajets.
- **url_stations** : URL contenant les données des stations.
- **fichier_sortie** *(optionnel)* : Nom du fichier CSV de sortie (par défaut : `Velomagg_avec_coordonnees.csv`).

### Méthodes

- **telecharger_et_nettoyer_trajets()**  
  Télécharge les données des trajets et nettoie les noms des stations avec des remplacements spécifiques.

- **ajouter_coordonnees_stations()**  
  Télécharge les données des stations et ajoute les coordonnées aux stations de départ et d'arrivée dans les données des trajets.

- **supprimer_lignes_manquantes()**  
  Supprime les lignes des trajets contenant des valeurs manquantes pour garantir des données complètes.

- **sauvegarder_csv()**  
  Sauvegarde les données enrichies dans un fichier CSV spécifié lors de l'initialisation.

- **executer()**  
  Exécute toutes les étapes du pipeline de traitement des données (dans l'ordre des méthodes mentionnées).

### Exemple d'utilisation

.. code-block:: python

    from traitement_donnee import TraitementDonneesVelomagg

    # Définir les URLs des données
    url_trajets = "https://drive.google.com/uc?id=1kUMForLXwdGvV9ha2Qx-vMd6CnoMnWV5"
    url_stations = "https://drive.google.com/uc?id=1HgOLf2JD46ZJlyrF_c99QZb6of6ajNYh"

    
    # Créer une instance de la classe
    traitement = TraitementDonneesVelomagg(
        url_trajets=url_trajets,
        url_stations=url_stations,
        fichier_sortie="donnees_velomagg.csv"
    )
    
    # Exécuter le traitement
    traitement.executer()

### Fichier de sortie

- Les données enrichies sont enregistrées dans le fichier CSV défini par **fichier_sortie**.
- Ce fichier contient les colonnes suivantes :
  - **Departure station**, **Departure**, **Return station**, **Return**
  - **Duration (sec.)**, **Covered distance (m)**
  - **latitude_depart**, **longitude_depart**, **latitude_retour**, **longitude_retour**

---

## Notes supplémentaires

- Les noms des stations sont nettoyés à l'aide d'un dictionnaire de remplacements spécifiques pour uniformiser les données.
- Les lignes avec des valeurs manquantes sont supprimées après ajout des coordonnées.

---
