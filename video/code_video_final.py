#%%
# meilleur code 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import osmnx as ox

# Charger les données depuis le fichier CSV
df = pd.read_csv("Velomagg_2023_with_coords.csv", parse_dates=["Departure", "Return"])

# Charger la carte de Montpellier avec fond noir
ox.settings.use_cache = True
G = ox.graph_from_place("Montpellier, France", network_type="bike")

# Créer la figure avec fond noir
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_facecolor("black")
ox.plot_graph(G, ax=ax, node_size=0, edge_color="gray", edge_alpha=0.3, show=False, close=False)

# Initialiser des structures pour les vélos et les trajets
bike_points = ax.scatter([], [], c="white", s=50, zorder=3)
line_data = {}  # Stockage des lignes représentant les trajets
time_text = ax.text(0.5, 0.95, "", ha="center", va="center", color="white", fontsize=12, transform=ax.transAxes)

# Fonction pour calculer les itinéraires
def calculate_routes(row):
    origin = (row["departure_latitude"], row["departure_longitude"])
    destination = (row["return_latitude"], row["return_longitude"])
    try:
        origin_node = ox.nearest_nodes(G, origin[1], origin[0])
        destination_node = ox.nearest_nodes(G, destination[1], destination[0])
        route = ox.routing.shortest_path(G, origin_node, destination_node)
        return route
    except Exception:
        return []

df["route"] = df.apply(calculate_routes, axis=1)

# Fonction pour mettre à jour l'animation
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

            # Position actuelle du vélo
            current_node = route[progress]
            x, y = G.nodes[current_node]["x"], G.nodes[current_node]["y"]
            bike_positions.append((x, y))

            # Traçage du trajet déjà parcouru
            if progress > 0:
                route_segment = route[:progress + 1]
                segment_coords = [(G.nodes[node]["x"], G.nodes[node]["y"]) for node in route_segment]

                if trip.name not in line_data:
                    # Ajouter une nouvelle ligne pour ce trajet
                    line_data[trip.name] = ax.plot(
                        [coord[0] for coord in segment_coords],
                        [coord[1] for coord in segment_coords],
                        c="blue",
                        alpha=0.3,
                        linewidth=2,
                        zorder=2,
                    )[0]
                else:
                    # Mettre à jour la ligne existante
                    line_data[trip.name].set_data(
                        [coord[0] for coord in segment_coords],
                        [coord[1] for coord in segment_coords],
                    )

    if bike_positions:
        bike_points.set_offsets(bike_positions)

    # Mise à jour de l'heure et de la date
    time_text.set_text(f"Temps: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    return bike_points, list(line_data.values()), time_text

# Créer l'animation
ani = FuncAnimation(fig, update, frames=range(0, int(df["Duration (sec.)"].max() // 300) + 1), interval=100)

# Sauvegarder la vidéo
ani.save("bike_animation_with_routes.mp4", fps=10, writer="ffmpeg")
plt.show()

# %%
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import osmnx as ox
from moviepy.editor import VideoFileClip, AudioFileClip

# Charger les données depuis le fichier CSV
df = pd.read_csv("Velomagg_2023_with_coords.csv", parse_dates=["Departure", "Return"])

# Charger la carte de Montpellier avec fond noir
ox.settings.use_cache = True
G = ox.graph_from_place("Montpellier, France", network_type="bike")

# Créer la figure avec fond noir
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_facecolor("black")
ox.plot_graph(G, ax=ax, node_size=0, edge_color="gray", edge_alpha=0.3, show=False, close=False)

# Initialiser des structures pour les vélos et les trajets
bike_points = ax.scatter([], [], c="white", s=50, zorder=3)
line_data = {}
time_text = ax.text(0.5, 0.95, "", ha="center", va="center", color="white", fontsize=12, transform=ax.transAxes)

# Fonction pour calculer les itinéraires
def calculate_routes(row):
    origin = (row["departure_latitude"], row["departure_longitude"])
    destination = (row["return_latitude"], row["return_longitude"])
    try:
        origin_node = ox.nearest_nodes(G, origin[1], origin[0])
        destination_node = ox.nearest_nodes(G, destination[1], destination[0])
        route = ox.routing.shortest_path(G, origin_node, destination_node)
        return route
    except Exception:
        return []

df["route"] = df.apply(calculate_routes, axis=1)

# Fonction pour mettre à jour l'animation
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

            # Position actuelle du vélo
            current_node = route[progress]
            x, y = G.nodes[current_node]["x"], G.nodes[current_node]["y"]
            bike_positions.append((x, y))

            # Traçage du trajet déjà parcouru
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
ani = FuncAnimation(fig, update, frames=range(0, int(df["Duration (sec.)"].max() // 300) + 1), interval=100)

# Sauvegarder la vidéo sans son
video_path = "bike_animation_with_routes.mp4"
ani.save(video_path, fps=10, writer="ffmpeg")
plt.close()

# Ajouter une bande sonore à la vidéo
audio_path = "background_music.mp3"  # Ton fichier audio
final_video_path = "bike_animation_with_sound.mp4"

video_clip = VideoFileClip(video_path)
audio_clip = AudioFileClip(audio_path).set_duration(video_clip.duration)
final_clip = video_clip.set_audio(audio_clip)

# Sauvegarder la vidéo finale avec le son
final_clip.write_videofile(final_video_path, codec="libx264", audio_codec="aac")


# %%
