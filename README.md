# CIRCULATION DES VÉLOS À MONTPELLIER

## INTRODUCTION
À Montpellier, le choix des transports est nombreux, mais le vélo reste l'une des options les plus écologiques et pratiques. Cela est notamment dû à Vélomagg, qui propose des vélos en libre-service à différents endroits de la ville.
Dans ce projet, nous nous limiterons à Montpellier et toutes nos observations seront rassemblées sur un site web. Nous souhaitons visualiser le trafic cycliste sur une année tout en prédisant ce trafic pour le lendemain afin que toute personne se déplacant à vélo puisse savoir par quels chemins passer.

## SITE INTERNET
Le site est disponible à l'adresse suivante :
https://coralieromani.github.io/PROJET_2024/

## OBJECTIFS et Contexte
Le projet porte sur l'analyse des déplacements de vélos dans Montpellier, en utilisant des ensembles de données publiques disponibles, tels que :  \
      -Trajets en vélos partagés : Les trajets des vélos VéloMagg.\
      -Comptage de cyclistes et piétons : Données issues des capteurs de vélo.\
      -Données OpenStreetMap : Pour cartographier les infrastructures et les trajets.\
Le but est de créer un site web interactif permettant de visualiser ces données et de faire des prédictions sur le trafic de vélos pour les jours qui vont suivre. Les résultats attendus incluent :

1) Un site web avec des cartes et des graphiques permettant de visualiser ces données de manière intuitive.
2) Une présentation vidéo (similaire à celle de NYC CitiBike) illustrant les tendances de trafic.
3) Un système prédictif pour anticiper le trafic avec un code couleur, à la manière de Bison Futé.
4) une analyse sur le trafic cycliste à Montpellier à l'aide de données ouvertes.
## Architecture du projet

### Fichiers et dossiers principaux

- `my_module_name/` : Dossier contenant les scripts Python pour l'analyse des données.\
- `telechargement_données.py` : Script pour télécharger et préparer les données.\
- `visualisation.py` : Script pour la création des graphiques et des cartes interactives.\
- `prediction.py` : Contient le modèle de prédiction du trafic .\
 - `données_traffic.py` : Classe principale pour la gestion des données.\
- `gantt/` : Contiendra le fichier du diagramme de Gantt pour la planification.\
- `siteweb/` : Contient les fichiers pour la création du site web interactif.\
- `.gitignore` : Fichier pour ignorer les fichiers inutiles.\
- `README.md` : Description générale du projet.
### Branches Git

- **base des données** : Branche dédiée au téléchargement et à la préparation des jeux de données.\
- **diagramme de Gantt** : Branche dédiée à la gestion du planning via un diagramme de Gantt.\
- **site web** : Branche pour le développement du site web interactif.

## COMMENT ON PROCEDE
1. **Téléchargement et traitement des données** : Depuis les sources VéloMagg, comptages de cyclistes et OpenStreetMap.
2. **Planification du projet** : Création du diagramme de Gantt pour organiser les tâches.\
3. **Création des visualisations** : Graphiques temporels, cartes de densité, cartes interactives.\
4. **Modélisation prédictive** : Modèles de séries temporelles pour prédire le trafic cycliste.\
5. **Développement du site web** : Hébergement des résultats interactifs via GitHub Pages.
## REPARTITION DES TÂCHES
- Créer un site web -> Samy
- Le diagramme de gantt -> DIALLO
- Base de données comptage cycliste et pieton -> Rokhaya
- Base de donné Open street map -> Coralie
- Base de donné Balades en partage de vélo -> a definir
- Cartographier Montpellier


## STRUCTURE
### Architecture du site
### Description des données 
### Package 

Structure du projet (documents, codes sources, ... séparés)

## DOCUMENTATION


## 1er approche 
- Créer un diagramme de gantt (diagramme qui permet de lister les tâches et de créer un planning à respecter)
- Créer un site web avec la carte, le diagramme,...
- Créer les branches: diagramme, site web, 3 bases de données 
- Décrire les packages et les logiciels 
