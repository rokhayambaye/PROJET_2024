import plotly.express as px
import pandas as pd

# Création des données
df = pd.DataFrame({
    'Task': ["Diagramme", "Site Web", "BD C_Cycliste", "BD O_Streetmap","BD Balades","Cart_Montpellier"],
    'Start': ["2024-10-01", "2024-10-04", "2024-10-06", "2024-10-10","2024-10-13","2024-10-17"],
    'Finish': ["2024-10-04", "2024-10-06", "2024-10-10", "2024-10-13","2024-10-17","2024-10-20"],
    'Status': ["Terminé", "En cours", "Terminé", "Terminé","Terminé","En cours"]
})

# Convertir les colonnes de dates en format datetime
df['Start'] = pd.to_datetime(df['Start'])
df['Finish'] = pd.to_datetime(df['Finish'])

# Création du diagramme de Gantt avec plotly.express
fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Status")

# Personnaliser l'affichage
fig.update_layout(title="Diagramme de Gantt", xaxis_title="Date", yaxis_title="Tâches")

# Affichage du diagramme
fig.show()

