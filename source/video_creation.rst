Gestion des Vidéos : Déplacements des Vélos à Montpellier
=========================================================

Ce document décrit les scripts et fonctions permettant de créer des vidéos animées des déplacements des vélos à Montpellier et d'ajouter une bande sonore aux vidéos générées.

Tous les scripts et fonctions décrits ici se trouvent dans le dossier suivant :  
**bike/video**

Création de l'Animation
------------------------

Le script `code_video_date.py` génère une animation montrant les déplacements des vélos à Montpellier sur une journée spécifique, en utilisant les données de trajets et un fond de carte d'OpenStreetMap.

Fonctionnalités
----------------
- Chargement des données depuis un fichier CSV contenant les trajets.
- Filtrage des trajets selon des critères temporels et de durée.
- Génération d'un graphe routier de Montpellier via **osmnx**.
- Création d'une animation des vélos et des trajets en temps simulé.
- Sauvegarde de l'animation au format vidéo.

Dépendances
------------
Ce script utilise les bibliothèques suivantes :
    - **pandas**

    - **matplotlib**

    - **osmnx**

**Génération de la Vidéo pour le 12 Mai 2023**

Ce code génère une vidéo représentant les déplacements des vélos le **12 mai 2023**. Voici le script utilisé :

Code Source
------------
.. code-block:: python

    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    import osmnx as ox

    # Charger les données depuis le fichier CSV
    df = pd.read_csv("https://drive.google.com/uc?id=1tS82dn4_n_yjaXe8iCaKtF6vgY1GpgpY", parse_dates=["Departure", "Return"])

    # Filtrer les données pour une journée spécifique et exclure les trajets trop longs ou trop courts
    df = df[(df["Departure"].dt.date == pd.to_datetime("2023-05-12").date()) &
            (df["Return"].dt.date == pd.to_datetime("2023-05-12").date()) &
            ((df["Return"] - df["Departure"]).dt.total_seconds() <= 86400)]
    df["duration"] = (df["Return"] - df["Departure"]).dt.total_seconds()
    df = df[df["duration"] > 10]  # Trajets supérieurs à 10 secondes

    # Charger la carte de Montpellier avec un style prédéfini
    ox.settings.use_cache = True
    G = ox.graph_from_place("Montpellier, France", network_type="bike")

    # Créer la figure avec fond noir
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_facecolor("black")
    ox.plot_graph(G, ax=ax, node_size=0, edge_color="gray", edge_alpha=0.3, show=False, close=False)

    # Initialiser des structures pour l'animation
    bike_points = ax.scatter([], [], c="white", s=50, zorder=3)
    line_data = {}
    time_text = ax.text(0.5, 0.95, "", ha="center", va="center", color="white", fontsize=12, transform=ax.transAxes)

    def calculate_routes(row):
        origin = (row["latitude_depart"], row["longitude_depart"])
        destination = (row["latitude_retour"], row["longitude_retour"])
        try:
            origin_node = ox.nearest_nodes(G, origin[1], origin[0])
            destination_node = ox.nearest_nodes(G, destination[1], destination[0])
            route = ox.routing.shortest_path(G, origin_node, destination_node)
            return route
        except Exception:
            return []

    df["route"] = df.apply(calculate_routes, axis=1)

    def update(frame):
        current_time = df["Departure"].min() + pd.Timedelta(seconds=frame * 300)
        active_trips = df[(df["Departure"] <= current_time) & (df["Return"] >= current_time)]
        bike_positions = []

        for _, trip in active_trips.iterrows():
            if trip["route"]:
                route = trip["route"]
                trip_duration = (trip["Return"] - trip["Departure"]).total_seconds()
                elapsed_time = (current_time - trip["Departure"]).total_seconds()
                progress = min(int((elapsed_time / trip_duration) * (len(route) - 1)), len(route) - 1)

                current_node = route[progress]
                x, y = G.nodes[current_node]["x"], G.nodes[current_node]["y"]
                bike_positions.append((x, y))

                if progress > 0:
                    route_segment = route[:progress + 1]
                    segment_coords = [(G.nodes[node]["x"], G.nodes[node]["y"]) for node in route_segment]

                    if trip.name not in line_data:
                        line_data[trip.name] = ax.plot(
                            [coord[0] for coord in segment_coords],
                            [coord[1] for coord in segment_coords],
                            c="blue",
                            alpha=0.3,
                            linewidth=2,
                            zorder=2,
                        )[0]
                    else:
                        line_data[trip.name].set_data(
                            [coord[0] for coord in segment_coords],
                            [coord[1] for coord in segment_coords],
                        )

        if bike_positions:
            bike_points.set_offsets(bike_positions)
            time_text.set_text(f"Temps: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        return bike_points, list(line_data.values()), time_text

    # Créer l'animation
    frames = range(0, int((df["Return"].max() - df["Departure"].min()).total_seconds() // 300) + 1)
    ani = FuncAnimation(fig, update, frames=frames, interval=200)
    # Sauvegarder la vidéo
    ani.save("bike_animation_12_Mai.mp4", fps=5, writer="ffmpeg")
    plt.show()

**Génération de la Vidéo pour le 14 Mai 2023**

Pour générer la vidéo des déplacements des vélos pour le **14 mai 2023**, le même script est utilisé, à l'exception de la date. Voici les modifications apportées :

.. code-block:: python

   # Charger les données pour le 14 mai 2023
   df = pd.read_csv("https://drive.google.com/uc?id=1tS82dn4_n_yjaXe8iCaKtF6vgY1GpgpY", parse_dates=["Departure", "Return"])
   df = df[(df["Departure"].dt.date == pd.to_datetime("2023-05-14").date()) &
           (df["Return"].dt.date == pd.to_datetime("2023-05-14").date()) &
           ((df["Return"] - df["Departure"]).dt.total_seconds() <= 86400)]
   df["duration"] = (df["Return"] - df["Departure"]).dt.total_seconds()
   df = df[df["duration"] > 10]

   # Reste du code identique : création de la carte et animation.
   ani.save("bike_animation_14_Mai.mp4", fps=5, writer="ffmpeg")

**Résultat**

Les animations génèrent deux vidéos représentant les déplacements des vélos :  

1. **12 mai 2023 :** Sauvegardée sous le nom `bike_animation_12_Mai.mp4`.
2. **14 mai 2023 :** Sauvegardée sous le nom `bike_animation_14_Mai.mp4`.


Ajout de Musique à la Vidéo
---------------------------

**Description :**  
Cette fonction ajoute une piste audio à une vidéo générée, en ajustant la durée de l'audio pour correspondre à celle de la vidéo. Si nécessaire, l'audio est coupé ou répété.

**Prototype :**  
.. code-block:: python

   def add_music_to_video(video_path, audio_path, output_video_with_audio_path, duration):

**Paramètres :**

- **video_path** *(str)* : Chemin du fichier vidéo d'entrée.
- **audio_path** *(str)* : Chemin du fichier audio d'entrée.
- **output_video_with_audio_path** *(str)* : Chemin pour sauvegarder la vidéo avec audio ajouté.
- **duration** *(int ou float)* : Durée souhaitée de la vidéo et de l'audio en secondes.

**Code Source :**

.. code-block:: python

   from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips

   def add_music_to_video(video_path, audio_path, output_video_with_audio_path, duration):
       import os
       if not os.path.isfile(video_path):
           print(f"Erreur : La vidéo '{video_path}' est introuvable.")
           return
       if not os.path.isfile(audio_path):
           print(f"Erreur : L'audio '{audio_path}' est introuvable.")
           return

       try:
           video_clip = VideoFileClip(video_path).subclip(0, duration)
           audio_clip = AudioFileClip(audio_path)

           if audio_clip.duration > duration:
               audio_clip = audio_clip.subclip(0, duration)
           elif audio_clip.duration < duration:
               num_loops = int(duration // audio_clip.duration) + 1
               audio_clip = concatenate_audioclips([audio_clip] * num_loops).subclip(0, duration)

           video_with_audio = video_clip.set_audio(audio_clip)
           video_with_audio.write_videofile(output_video_with_audio_path, codec="libx264", audio_codec="aac")
           print(f"Vidéo avec musique créée avec succès : {output_video_with_audio_path}")

       except Exception as e:
           print(f"Erreur inattendue : {e}")

**Exemple d'utilisation :**

Pour ajouter une musique à chacune des vidéos générées :  

.. code-block:: python

   add_music_to_video(
       video_path="bike_animation_12_Mai.mp4",
       audio_path="bike/video/musique.mp3",
       output_video_with_audio_path="bike_animation_12_Mai_son.mp4",
       duration=57
   )

   add_music_to_video(
       video_path="bike_animation_14_Mai.mp4",
       audio_path="bike/video/musique.mp3",
       output_video_with_audio_path="bike_animation_14_Mai_son.mp4",
       duration=57
   )

**Messages d'erreurs potentiellles :**

- Si le fichier vidéo ou audio est introuvable :

  .. code-block:: text

     Erreur : La vidéo '<chemin>' est introuvable.
     Erreur : L'audio '<chemin>' est introuvable.

- En cas d'erreur inattendue :

  .. code-block:: text

     Erreur inattendue : <détails de l'exception>


.. note::

   Assurez-vous que les données d'entrée `Velomagg_avec_coordonnees.csv` sont correctement formatées et placées dans le même répertoire que le script.

