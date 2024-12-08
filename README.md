---
title: "ANALYSE DU TRAFIC CYCLISTE"
author: "DIALLO Ousmane , M'RAD Samy , MBAYE Rokhaya, ROMANI DE VINCI Coralie"
format: markdown
---

# **description**

Ce module analyse et visualise le trafic cycliste à Montpellier, en s'appuyant sur les trajets des vélos VéloMagg, les comptages des éco-compteurs, et les données cartographiques d'OpenStreetMap.  
Grâce à des animations, des cartes interactives et des prédictions de trafic, ce projet offre une exploration complète des données liées aux déplacements à vélo dans la région.

---
### **Installation**
Pour installer ce module, exécutez la commande suivante :
```bash
$ pip install git+https://github.com/coralieromani/PROJET_2024
```
### **Documentation**
La documentation complète est disponible [ici](https://lien..). Elle inclut :
- Une introduction détaillée au projet.
- Des tutoriels pour le traitement des données et la création de vidéos.
- Une description complète des classes et fonctions du projet.
# Structure du Projet

Le projet est organisé en plusieurs dossiers pour faciliter le développement, la maintenance et l’utilisation. Voici la structure détaillée :

## 1. Dossier `bike`
Ce dossier contient les fonctionnalités principales du projet, réparties dans différents sous-dossiers :

- `bike/Base_des_donnees` : Contient les scripts pour le téléchargement et le traitement des bases de données, y compris :
  - Les données VéloMagg.
  - Les données des éco-compteurs.

- `bike/video` : Contient le script utilisé pour créer des vidéos animées représentant les déplacements à vélo.

- `bike/carte` : Contient le script pour générer des cartes interactives.

- `bike/diagramme` : Contient les scripts pour produire des diagrammes visuels permettant d'analyser le trafic à vélo et d'autres données.

---

## 2. Dossier `roadmap`
Ce dossier regroupe les éléments liés à la planification du projet :

- `README.md` : Documentation générale décrivant les objectifs et la structure du projet.
- `diagramme_de_gantt.png` : Diagramme de Gantt illustrant la planification du projet.

---

## 3. Dossier `docs`
Ce dossier contient tous les fichiers HTML générés, y compris ceux liés aux cartes interactives, aux diagrammes et au site web du projet.

---

## 4. Dossier `slide`
Ce dossier contient les diapositives utilisées pour les présentations du projet. Ces diapositives sont créées avec Quarto.

---

## 5. Dossier `source`
Ce dossier est utilisé pour créer la documentation du projet, en s’appuyant sur des outils comme Sphinx.

---

## 6. Dossier `build`
Ce dossier contient les fichiers HTML générés à partir de la documentation située dans le dossier `source`.

---

## 7. Dossier `tests`
Les tests pour valider le bon fonctionnement des scripts et des fonctions du projet sont implémentés ici. Ils assurent la fiabilité du code et la qualité des développements.

---

## 8. Dossier `.github/workflows`
Ce dossier contient un workflow d’intégration continue. Ce dernier exécute des tests automatiquement chaque jour à 5 h du matin et à chaque contribution (push) dans le dépôt Git.

---

### Notes supplémentaires
- Chaque partie du projet est soigneusement séparée dans des sous-dossiers spécifiques pour garantir une bonne modularité et lisibilité.
- La documentation générée dans `docs` peut être consultée pour avoir un aperçu complet des résultats du projet.
- Le diagramme de Gantt et les diapositives facilitent la communication et la présentation des progrès du projet.

---

## Auteur
Ce projet a été réalisé dans le cadre d'un travail académique, avec une approche collaborative pour développer un système de gestion et d’analyse des données de partage de vélos.
