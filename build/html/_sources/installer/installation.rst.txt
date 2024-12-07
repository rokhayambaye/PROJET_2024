Installation du Projet
======================

Ce guide explique comment installer et configurer le projet pour démarrer rapidement.

Prérequis
---------
Avant de commencer, assurez-vous que les éléments suivants sont installés sur votre machine :

- Python 3.8 ou version ultérieure
- pip (gestionnaire de paquets Python)
- Git

Étapes d'installation
---------------------
1. **Cloner le dépôt Git** :
   Clonez le dépôt à l'aide de la commande suivante :git clone https://github.com/coralieromani/PROJET_2024 

2. **Créer un environnement virtuel** :
Créez un environnement virtuel pour isoler les dépendances du projet :
python -m venv env source env/bin/activate # Sur macOS/Linux env\Scripts\activate # Sur Windows

3. **Installer les dépendances** :
Installez toutes les dépendances nécessaires en exécutant :
pip install -r requirements.txt