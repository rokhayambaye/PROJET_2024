import pandas as pd
import plotly.graph_objects as go

# Charger les données
url_fichier = "https://drive.google.com/uc?id=19VIXjfEULKNq7ad2F9yz2b6qLDxG9D11"
velomagg_data = pd.read_csv(url_fichier)

# Convertir les colonnes de date en format datetime
velomagg_data['Departure'] = pd.to_datetime(velomagg_data['Departure'])

# Extraire les jours pour regrouper les données
velomagg_data['Day'] = velomagg_data['Departure'].dt.date

# Calculer le nombre de locations par jour
nb_location = velomagg_data.groupby('Day').size()

# Créer un graphique interactif
fig = go.Figure()

# Ajouter les locations par jour (courbe orange)
fig.add_trace(go.Scatter(
    x=nb_location.index, 
    y=nb_location.values, 
    mode='lines+markers',
    name='Locations par jour',
    line=dict(color='orange'),
    marker=dict(size=6),
    yaxis='y1'
))

# Mise en page avec 
fig.update_layout(
    title='Nombre de locations de vélomaag 2023 par jour',
    xaxis=dict(title='Date'),
    yaxis=dict(
        title='Nombre de locations',
        titlefont=dict(color='orange'),
        tickfont=dict(color='orange')
    ),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    hovermode='x unified'
)

# Sauvegarder et afficher le graphique
fig.write_html("docs/Diagramme/locations_et_temperature_interactif.html")
fig.show()
