import pandas as pd
import plotly.graph_objects as go

# Charger les données
file_path = 'Base_des_donnees/donnees_montpellier_2023.csv'  
Donnees_montpellier = pd.read_csv(file_path, sep=';')  # Ajouter le séparateur correct si nécessaire

# Convertir la colonne 'date' en format datetime
Donnees_montpellier['date'] = pd.to_datetime(Donnees_montpellier['date'])

# Regrouper par date et calculer la somme des intensités
flux_global = Donnees_montpellier.groupby('date')['intensity'].sum()

# Créer un graphique interactif avec Plotly
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=flux_global.index,
    y=flux_global.values,
    mode='lines+markers',
    name='Flux de vélos'
))

# Ajouter des détails au graphique
fig.update_layout(
    title='Flux global des vélos par jour à Montpellier (2023)',
    xaxis_title='Date',
    yaxis_title='Nombre de vélos',
    template='plotly_white',
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True),
    height=500
)

# Sauvegarder et afficher le graphique
fig.write_html("Diagramme/Diagramme_Flux_2023.html")
fig.show()