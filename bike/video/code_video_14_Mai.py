
#%%
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import osmnx as ox

# Charger les données depuis le fichier CSV
df = pd.read_csv("https://drive.google.com/uc?id=1tS82dn4_n_yjaXe8iCaKtF6vgY1GpgpY", parse_dates=["Departure", "Return"])
"""

Ce script traite les données de trajets de vélos partagés pour une animation représentant 
les déplacements à Montpellier, France, sur une journée spécifique.

Étapes principales :
1. Filtrer les trajets pour le 14 mai 2023.
2. Exclure les trajets trop longs (plus de 24h) ou trop courts (moins de 10 secondes).
"""
# Filtrer les données pour une journée spécifique et exclure les trajets trop longs ou trop courts
df = df[(df["Departure"].dt.date == pd.to_datetime("2023-05-14").date()) & 
        (df["Return"].dt.date == pd.to_datetime("2023-05-14").date()) & 
        ((df["Return"] - df["Departure"]).dt.total_seconds() <= 86400)]
df["duration"] = (df["Return"] - df["Departure"]).dt.total_seconds()
df = df[df["duration"] > 10]  # Trajets supérieurs à 10 secondes
"""

utilisation d'OSMnx pour générer un graphe représentant les routes adaptées aux vélos
dans la ville de Montpellier."""
# Charger la carte de Montpellier avec un style prédéfini
ox.settings.use_cache = True
G = ox.graph_from_place("Montpellier, France", network_type="bike")
 
"""
Création de la figure pour l'animation.

La figure est initialisée avec un fond noir et des paramètres de style pour les nœuds et arêtes.
Des structures comme `bike_points` sont également préparées pour l'affichage dynamique.
"""
# Créer la figure avec fond noir
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_facecolor("black")
ox.plot_graph(G, ax=ax, node_size=0, edge_color="gray", edge_alpha=0.3, show=False, close=False)

# Initialiser des structures pour l'animation
bike_points = ax.scatter([], [], c="white", s=50, zorder=3)
line_data = {}
time_text = ax.text(0.5, 0.95, "", ha="center", va="center", color="white", fontsize=12, transform=ax.transAxes)

def calculate_routes(row):
    """
    Calcule le chemin le plus court entre les points de départ et d'arrivée d'un trajet.

    Paramètres:
    -----------
    row : pandas.Series
        Ligne du DataFrame contenant les colonnes `latitude_depart`, `longitude_depart`,
        `latitude_retour`, et `longitude_retour`.

    Sortie :
    ---------
    Retourne une liste de nœuds représentant l'itinéraire sur le graphe.
    Retourne une liste vide si un chemin ne peut pas être calculé.
    """
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
    """
    Met à jour l'animation pour un instant donné.

    Paramètres:
    -----------
    frame : int
        Numéro du frame actuel, correspondant à un pas de temps (toutes les 300 secondes).

    Sortie :
    ---------
    
    Retourne les objets graphiques mis à jour (positions des vélos, segments de trajets et texte temporel).
    """
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

"""
Création et sauvegarde de l'animation.

La fonction `FuncAnimation` est utilisée pour générer une animation où les vélos
se déplacent sur la carte de Montpellier en fonction des données de trajets.
"""
# Créer l'animation
frames = range(0, int((df["Return"].max() - df["Departure"].min()).total_seconds() // 300) + 1)
ani = FuncAnimation(fig, update, frames=frames, interval=200)

# Sauvegarder la vidéo
ani.save("docs/Video/bike_animation_14_Mai.mp4", fps=5, writer="ffmpeg")
plt.show()

# %%
