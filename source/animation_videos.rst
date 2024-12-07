Animation des trajets de vélos à Montpellier
============================================

Ce script génère une animation des trajets de vélos à Montpellier à partir des données de trajets extraites d'un fichier CSV. Il utilise la bibliothèque `osmnx` pour charger la carte de Montpellier et calcule les itinéraires les plus courts entre les points de départ et d'arrivée des trajets de vélos. Ensuite, il génère une animation montrant les trajets actifs à différents moments de la journée.

Le script suit ces étapes principales :
1. Chargement des données de trajets de vélos depuis un fichier CSV.
2. Filtrage des trajets en fonction de la durée et de la date.
3. Calcul des itinéraires sur une carte OpenStreetMap.
4. Animation des trajets et génération d'une vidéo de l'animation.

Dépendances :
-------------
- pandas
- matplotlib
- matplotlib.animation
- osmnx

Fonctions
---------

**`calculate_routes(row)`**
    Calcule l'itinéraire le plus court entre le point de départ et le point d'arrivée d'un trajet.

    Args :
        row (pd.Series) : Ligne contenant les coordonnées de départ et d'arrivée.
        
    Retourne :
        list : Liste des nœuds représentant le chemin le plus court, ou une liste vide en cas d'échec.

**`update(frame)`**
    Met à jour les éléments de l'animation pour une frame donnée.

    Args :
        frame (int) : Numéro de la frame actuelle.
        
    Retourne :
        tuple : Objets graphiques à mettre à jour (points de vélos, lignes des trajets, texte du temps).

Exécution du script
-------------------

Le script charge les données depuis le fichier `velomagg-12-15.csv`, filtre les trajets pour une journée spécifique et exclut les trajets trop courts ou trop longs. Ensuite, il crée une animation en mettant à jour les positions des vélos à chaque frame. L'animation est ensuite enregistrée sous forme de vidéo au format MP4.

Le fichier CSV doit contenir les colonnes suivantes :
- **Departure** : Heure de départ du trajet.
- **Return** : Heure de retour du trajet.
- **latitude_depart** : Latitude du point de départ.
- **longitude_depart** : Longitude du point de départ.
- **latitude_retour** : Latitude du point de retour.
- **longitude_retour** : Longitude du point de retour.

Exemple de commande pour exécuter le script :

Résultat :
----------
Une vidéo `bike_animation_15_Dec.mp4` sera générée, montrant les trajets de vélos actifs à différents moments de la journée.

