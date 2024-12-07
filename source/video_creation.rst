Création de la Vidéo des Déplacements
=====================================

Ce script permet de générer une animation montrant les déplacements des vélos à Montpellier sur une journée spécifique, en utilisant les données de trajets et un fond de carte d'OpenStreetMap.

Fonctionnalités
----------------
- Chargement des données depuis un fichier CSV contenant les trajets.
- Filtrage des trajets selon des critères temporels et de durée.
- Génération d'un graphe routier de Montpellier via `osmnx`.
- Création d'une animation des vélos et des trajets en temps simulé.
- Sauvegarde de l'animation au format vidéo.

Dépendances
------------
Ce script utilise les bibliothèques suivantes :
- `pandas`
- `matplotlib`
- `osmnx`

Code Source
------------
.. code-block:: python

    #%%
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    import osmnx as ox

    # Charger les données depuis le fichier CSV
    df = pd.read_csv("Velomagg_avec_coordonnees.csv", parse_dates=["Departure", "Return"])

    # (Insérez ici le reste de votre script.)

Résultat
---------
L'animation génère une vidéo des déplacements des vélos pour le 12 mai 2023, montrant en temps réel les trajets des utilisateurs.

.. note::

   Assurez-vous que les données d'entrée `Velomagg_avec_coordonnees.csv` sont correctement formatées et placées dans le même répertoire que le script.

