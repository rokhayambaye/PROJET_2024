import pandas as pd
import plotly.graph_objects as go

# Charger les données
file_path = 'Base_des_donnees/CoursesVelomagg.csv'  
velomagg_data = pd.read_csv(file_path)

# Convertir les colonnes de date en format datetime
velomagg_data['Departure'] = pd.to_datetime(velomagg_data['Departure'])

# Extraire les jours pour regrouper les données
velomagg_data['Day'] = velomagg_data['Departure'].dt.date

# Calculer la température moyenne par jour
moy_temp = velomagg_data.groupby('Day')['Departure temperature (°C)'].mean()
# Calculer le nombre de locations par jour
nb_location = velomagg_data.groupby('Day').size()

# Créer un graphique interactif avec deux axes
fig = go.Figure()

# Ajouter les locations par jour (courbe bleue)
fig.add_trace(go.Scatter(
    x=nb_location.index, 
    y=nb_location.values, 
    mode='lines+markers',
    name='Locations par jour',
    line=dict(color='blue'),
    marker=dict(size=6),
    yaxis='y1'
))

# Ajouter la température moyenne (courbe rouge)
fig.add_trace(go.Scatter(
    x=moy_temp.index, 
    y=moy_temp.values, 
    mode='lines+markers',
    name='Température moyenne (°C)',
    line=dict(color='red'),
    marker=dict(size=6),
    yaxis='y2'
))

# Mise en page avec deux axes (location et temp)
fig.update_layout(
    title='Nombre de locations de vélomaag et température moyenne par jour',
    xaxis=dict(title='Date'),
    yaxis=dict(
        title='Nombre de locations',
        titlefont=dict(color='blue'),
        tickfont=dict(color='blue')
    ),
    yaxis2=dict(
        title='Température moyenne (°C)',
        titlefont=dict(color='red'),
        tickfont=dict(color='red'),
        anchor='x',
        overlaying='y',
        side='right'
    ),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    hovermode='x unified'
)

# Sauvegarder et afficher le graphique
fig.write_html("Diagramme/locations_et_temperature_interactif.html")
fig.show()
