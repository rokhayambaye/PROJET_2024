
# ANALYSE DU TRAFIC CYCLISTE🚴‍♀️

# **Description**

Ce module analyse et visualise le trafic cycliste à Montpellier, en s'appuyant sur les trajets des vélos VéloMagg, les comptages des éco-compteurs, et les données cartographiques d'OpenStreetMap.  
Grâce à des animations, des cartes interactives et des prédictions de trafic, ce projet offre une exploration complète des données liées aux déplacements à vélo dans la région.

---
# **Installation**
Pour installer ce module, exécutez la commande suivante :
```bash
$ pip install git+https://github.com/coralieromani/PROJET_2024
```
# **Site Web**
Le site est disponible à l'adresse suivante : https://coralieromani.github.io/PROJET_2024/
### Documentation
La documentation complète du projet  est disponible  sur notre site web.
Elle inclut :
- Une introduction détaillée au projet.
- Des tutoriels pour le traitement des données et la création de vidéos.
- Une description complète des classes et fonctions du projet.
### Extrait du code
Voici un extrait du code utilisé pour la création du site web :
```yaml
---
project:
  type: website
  output-dir: docs

title: "Trafic Cycliste à Montpellier"
format:
  html:
    toc: true  # Affichage d'une table des matières
    toc-title: "Sommaire"  # Titre personnalisé pour la table des matières
    code-fold: true  # Activation des blocs de code repliables
    css: styles.css  # Fichier CSS pour personnaliser le style
    theme: flatly  # Thème choisi pour l'apparence
---

<div id="logo-container" style="position: absolute; top: 10px; left: 10px;">
  <img src="https://us.123rf.com/450wm/aquir/aquir2307/aquir230700775/208710489-cycliste-cycliste-sur-route-illustration-dessinée-à-la-main-illustration-de-dessin-animé-de-style.jpg?ver=6" 
       alt="Cycliste sur route" 
       style="max-width: 150px; max-height: 100px;" 
       onclick="location.reload();" />
</div>
```
# **📜 Licence**
Ce projet est sous licence MIT, une licence permissive largement utilisée. Elle permet :

- Une utilisation libre du code, y compris pour des projets commerciaux.
- La modification et la redistribution du code, à condition de conserver les mentions de copyright et de licence.

Pour plus de détails, veuillez consulter le fichier [LICENSE](LICENSE).
# **Auteurs**
Ce projet a été réalisé par :
- **DIALLO Ousmane**
- **M'RAD Samy**
- **MBAYE Rokhaya**
- **ROMANI DE VINCI Coralie**
