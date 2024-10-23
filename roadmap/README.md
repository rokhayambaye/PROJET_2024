# ANALYSE DU TRAFIC CYCLISTE

## INTRODUCTION
À Montpellier, le choix des transports est nombreux, mais le vélo reste l'une des options les plus écologiques et pratiques. Cela est notamment dû à Vélomagg, qui propose des vélos en libre-service à différents endroits de la ville.
Dans ce projet, nous nous limiterons à Montpellier et toutes nos observations seront rassemblées sur un site web. Nous souhaitons visualiser le trafic cycliste sur une année tout en prédisant ce trafic pour le lendemain afin que toute personne se déplacant à vélo puisse savoir par quels chemins passer.

## SITE INTERNET
Le site est disponible à l'adresse suivante :
https://coralieromani.github.io/PROJET_2024/

## OBJECTIFS 
L'objectif principal est de développer des visualisations interactives sur un site web permettant d'explorer et de prédire les flux de vélos dans la ville. Les données exploitées inclueront les trajets du service VéloMagg, les comptages de cyclistes et piétons, ainsi que les informations cartographiques provenant d'OpenStreetMap.
Le projet sera réalisé en équipe, en veillant à une répartition équilibrée des tâches. 

## DESCRIPTION BASES DE DONNÉES 
### VéloMagg
VéloMagg est un service de location de vélos en libre-service qui nous permettra de visualiser le nombre de cyclistes et leurs trajets dans la ville. En effet, leur site nous fournit plusieurs données sur les vélos loués comme les stations de départ et d'arrivée mais aussi la durée de la location.


## Architecture du projet

### Fichiers et dossiers principaux
- `roadmap` : Contient les fichiers décrivant le projet, son architecture, et les étapes à suivre.
- `.github/workflows/` : Configuration des actions GitHub pour l'intégration continue et la création du site.
- `.gitignore` : Fichier pour ignorer les fichiers inutiles.
- `README.md` : Description générale du projet.
- `docs`: Contient les flichiers du site web (.qmd, .html, .css, images)

### Branches Git
- **Branche Main** : Branche principale contenant le code.
- **base des données** : Branche dédiée au téléchargement et à la préparation des bases de données.
- **diagramme de Gantt** : Branche dédiée à la gestion du planning via le diagramme de Gantt.
- **site web** : Branche pour le développement du site web.

### Logiciels utilisés
- **Python**:
Dans ce projet, Python sera utilisé pour analyser les bases de données liés au trafic cycliste, construire des modèles prédictifs pour estimer l’évolution du trafic, et développer des visualisations interactives. 

- **Quarto**:
Pour le développement du site web, nous utiliserons Quarto, qui facilitera sa création. Il offre également la possibilité d'intégrer des images, des documents et des rapports interactifs, ce qui sera utile pour le README. Quarto permet aussi de combiner du code Python avec du texte explicatif.

### Packages

- **Numpy** :
La bibliothèque Numpy de Python permet d'effectuer des calculs numériques mais aussi de traiter des matrices ou des tableaux multidimensionnels grâce aux fonction intégrées.

- **Pandas** :
Pandas permet de nettoyer et analyser rapidement des ensembles de données. On l'utilisera pour traiter les données des trajets du service VéloMagg et les comptages de cyclistes.

- **Pooch** :
Pooch est une bibliothèque Python permettant de télécharger des données à partir d'une URL et de les stocker.

- **Os** :
Os, qui est directement intégré dans Python, nous fournit une interface pour gérer les fichiers téléchargés.

- **Seaborn** :
Seaborn est une bibliothèque de Python, nous permettant de visualiser les données en facilitant la création des graphiques sur Matplotlib.

- **Folium** :
Folium permet de créer des cartes interactives pour visualiser les trajets cyclistes, ajouter des points d’intérêt (comme les stations Vélomagg), et délimiter des zones (comme -5 min, -10 min, etc.).

- **Leaflet** :
Leaflet est une bibliothèque JavaScript de cartographie qui nous permettra de créer la carte interactive grâce aux données récupérées sur OpenStreetMap.

## Répartition des tâches
- **Création du site web**: Développement d'une plateforme pour la publication et l'exploration interactive des résultats du projet, incluant des visualisations de données.
- **Élaboration du diagramme de Gantt** : Planification et suivi de l'avancement du projet à l'aide d'un diagramme de Gantt, afin d'assigner et gérer les différentes étapes et tâches.
- **Gestion des bases des données** : Collecte, traitement et analyse des données à partir des sources disponibles.
- **Cartographie de la ville de Montpellier** : Création de cartes interactives et visuelles pour représenter les données spatiales et leur répartition à Montpellier.
- **Video**: Création de la video des flux des cyclistes à Montpellier.
  