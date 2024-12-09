import pandas as pd
import plotly.graph_objects as go

# Charger les données
url_fichier = "https://drive.google.com/uc?id=19VIXjfEULKNq7ad2F9yz2b6qLDxG9D11"
velomagg_data = pd.read_csv(url_fichier)

# Convertir les colonnes de date en format datetime
velomagg_data['Departure'] = pd.to_datetime(velomagg_data['Departure'])

# Ajouter une colonne pour le mois
velomagg_data['Month'] = velomagg_data['Departure'].dt.month
mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

# Calculer le nombre moyen de locations par mois
locations_par_mois = velomagg_data.groupby('Month').size()

# Créer un graphique interactif pour les locations par mois
fig_mois = go.Figure()

fig_mois.add_trace(go.Bar(
    x=mois,
    y=locations_par_mois,
    name='Locations par mois',
    marker_color='orange'
))

fig_mois.update_layout(
    title='Nombre de locations Vélomagg par mois (2023)',
    xaxis_title='Mois',
    yaxis_title='Nombre de locations',
    template='plotly_white',
    height=500
)

fig_mois.write_html("docs/Diagramme/Diagramme_locations.html")
