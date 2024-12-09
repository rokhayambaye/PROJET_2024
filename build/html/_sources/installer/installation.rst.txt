Installation du Projet
======================

Ce guide explique comment installer et configurer le projet pour démarrer rapidement.

Prérequis
------------
Avant de commencer, assurez-vous d'installer  :

FFmpeg  requis pour générer les vidéos. Installez-le selon votre système d'exploitation :

- **Windows** : Téléchargez et configurez depuis `ffmpeg.org <https://ffmpeg.org/download.html>`_, puis ajoutez le dossier ``bin`` à la variable d'environnement ``PATH``.
- **Linux** : Installez avec votre gestionnaire de paquets :

  .. code-block:: bash

     sudo apt install ffmpeg

- **macOS** : Utilisez Homebrew :

  .. code-block:: bash

     brew install ffmpeg


Pour vérifier l'installation de FFmpeg, exécutez la commande suivante dans un terminal :

.. code-block:: bash

   ffmpeg -version

Étapes d'installation
---------------------
1. **Cloner le dépôt Git** :
   Clonez le dépôt à l'aide de la commande suivante :git clone https://github.com/coralieromani/PROJET_2024 
2. **Installer les dépendances** :

Installez les bibliothèques nécessaires via le fichier **requirements.txt** :

.. code-block:: bash

   pip install -r requirements.txt
