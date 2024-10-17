# ANALYSE DU TRAFIC CYCLISTE

## INTRODUCTION
À Montpellier, le choix des transports est nombreux, mais le vélo reste l'une des options les plus écologiques et pratiques. Cela est notamment dû à Vélomagg, qui propose des vélos en libre-service à différents endroits de la ville.
Dans ce projet, nous nous limiterons à Montpellier et toutes nos observations seront rassemblées sur un site web. Nous souhaitons visualiser le trafic cycliste sur une année tout en prédisant ce trafic pour le lendemain afin que toute personne se déplacant à vélo puisse savoir par quels chemins passer.

## SITE INTERNET
Le site est disponible à l'adresse suivante :
https://coralieromani.github.io/PROJET_2024/

## OBJECTIFS 
Ce projet vise à analyser le trafic cycliste à Montpellier en exploitant plusieurs jeux de données. L'objectif principal est de développer des visualisations interactives sur un site web permettant d'explorer et de prédire les flux de vélos dans la ville. Les données exploitées incluront les trajets du service VéloMagg, les comptages de cyclistes et piétons, ainsi que les informations cartographiques provenant d'OpenStreetMap.

Le projet sera réalisé en équipe, avec une gestion collaborative des contributions sur GitHub, en veillant à une répartition équilibrée des tâches. L'essentiel du travail portera sur la création de visualisations et la mise en place d'une interface web interactive pour faciliter la navigation et l'interprétation des résultats.


## Architecture du projet

### Fichiers et dossiers principaux

- `roadmap` : Contientles fichiers décrivant le projet, son architecture, et les étapes à suivre.
- `telechargement_données.py` : Script pour télécharger et préparer les données.
- `visualisation.py` : Script pour la création des graphiques et des cartes interactives.
- `prediction.py` : Contient le modèle de prédiction du trafic .
 - `données_traffic.py` : Classe principale pour la gestion des données.
- `siteweb/` : Contient les fichiers pour la création du site web interactif.
- `.gitignore` : Fichier pour ignorer les fichiers inutiles.
- `README.md` : Description générale du projet.
### Branches Git
- **Branche Main** : Branche principale contenant le code stable.
- **base des données** : Branche dédiée au téléchargement et à la préparation des jeux de données.
- **diagramme de Gantt** : Branche dédiée à la gestion du planning via un diagramme de Gantt.
- **site web** : Branche pour le développement du site web interactif.

### Packages et logiciels utilisés
- **Python**:
Python est un langage de programmation polyvalent, souvent utilisé dans le domaine de la science des données et de l'intelligence artificielle. Il offre une vaste gamme de bibliothèques pour l'analyse de données, la visualisation et la modélisation prédictive. Dans ce projet, Python sera utilisé pour analyser les jeux de données liés au trafic cycliste, construire des modèles prédictifs pour estimer l’évolution du trafic, et développer des visualisations interactives qui seront intégrées dans un site web. Sa flexibilité et sa large communauté en font un choix privilégié pour des projets de ce type.
- **Pandas** :
Pandas est une bibliothèque Python essentielle pour la manipulation et l’analyse de données structurées, notamment sous forme de tables (comme des fichiers CSV). Elle permet de filtrer, nettoyer, transformer et analyser rapidement des ensembles de données. Dans ce projet, Pandas sera utilisé pour traiter les données des trajets cyclistes du service VéloMagg et les comptages de cyclistes/piétons, en facilitant des opérations comme le calcul de statistiques descriptives, la gestion des valeurs manquantes, ou encore l’agrégation des données par jour ou par zones géographiques.
## Pipeline de développement
- Collecte et traitement des données : Récupération des données depuis les sources VéloMagg, les comptages de cyclistes et OpenStreetMap, suivie de leur préparation pour l'analyse.
- Planification du projet : Élaboration d'un diagramme de Gantt pour organiser et suivre les différentes tâches du projet.
- Conception des visualisations : Création de graphiques temporels, de cartes de densité et de cartes interactives pour représenter les données de manière claire.
- Prévision du trafic cycliste : Mise en place de modèles de séries temporelles pour anticiper les variations du trafic à vélo.
- Développement du site web : Publication des résultats interactifs et des visualisations sur GitHub Pages pour faciliter l'accès et l'exploration des données.
## REPARTITION DES TÂCHES
- Créer un site web -> Samy
- Le diagramme de gantt -> DIALLO
- Base de données comptage cycliste et pieton -> Rokhaya
- Base de donné Open street map -> Coralie
- Base de donné Balades en partage de vélo -> a definir
- Cartographier Montpellier