# %%
############################le bon code #########################
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
bike_points = ax.scatter([], [], c="white", s=50, zorder=3)  # Points des vélos
line_data = {}  # Trajets accumulés
time_text = ax.text(0.5, 0.95, "", ha="center", va="center", color="white", fontsize=12, transform=ax.transAxes)

# Fonction pour mettre à jour l'animation
def update(frame):
    current_time = df["Departure"].min() + pd.Timedelta(seconds=frame * 300)
    active_trips = df[(df["Departure"] <= current_time) & (df["Return"] >= current_time)]

    bike_positions = []  # Réinitialiser les positions des vélos pour chaque frame
    for _, trip in active_trips.iterrows():
        # Calculer la progression du vélo sur le trajet
        trip_duration = (trip["Return"] - trip["Departure"]).total_seconds()
        elapsed_time = (current_time - trip["Departure"]).total_seconds()
        progress = elapsed_time / trip_duration
        current_longitude = trip["departure_longitude"] + progress * (trip["return_longitude"] - trip["departure_longitude"])
        current_latitude = trip["departure_latitude"] + progress * (trip["return_latitude"] - trip["departure_latitude"])
        bike_positions.append([current_longitude, current_latitude])

        # Mise à jour des trajets
        line_key = (trip["departure_latitude"], trip["departure_longitude"], trip["return_latitude"], trip["return_longitude"])
        if line_key not in line_data:
            line_data[line_key] = ax.plot(
                [trip["departure_longitude"], trip["return_longitude"]],
                [trip["departure_latitude"], trip["return_latitude"]],
                c="blue",
                alpha=0.1,
                linewidth=1
            )[0]
        else:
            line_data[line_key].set_alpha(min(1.0, line_data[line_key].get_alpha() + 0.02))  # Intensifier

    if bike_positions:  # Vérifier si des positions sont disponibles
        bike_points.set_offsets(bike_positions)
    
    # Mise à jour de l'heure et de la date
    time_text.set_text(f"Temps: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    return bike_points, line_data.values(), time_text

# Créer l'animation
ani = FuncAnimation(fig, update, frames=range(0, int(df["Duration (sec.)"].max() // 300) + 1), interval=100)

# Sauvegarder la vidéo
ani.save("bike_animation_with_map.mp4", fps=10, writer="ffmpeg")
plt.show()

