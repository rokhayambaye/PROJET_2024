import pandas as pd
import plotly.graph_objects as go

# Charger les données
url_fichier = "https://drive.google.com/uc?id=1yJUkkGiobznF50tQaKwbM4a2bfiEVmRy"
Donnees_montpellier = pd.read_csv(url_fichier, sep=';')  # Ajouter le séparateur correct si nécessaire

# Convertir la colonne 'date' en format datetime
Donnees_montpellier['date'] = pd.to_datetime(Donnees_montpellier['date'])

# Ajouter une colonne pour le mois (1 = Janvier, 12 = Décembre)
Donnees_montpellier['month'] = Donnees_montpellier['date'].dt.month

# Calculer la moyenne des flux par mois
moyenne_par_mois = Donnees_montpellier.groupby('month')['intensity'].mean()

# Créer un graphique interactif pour afficher les résultats
mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

fig = go.Figure()

fig.add_trace(go.Bar(
    x=mois,
    y=moyenne_par_mois,
    name='Moyenne des flux',
    marker_color='green'
))

# Ajouter des détails au graphique
fig.update_layout(
    title='Moyenne des flux de vélos par mois (2023)',
    xaxis_title='Mois',
    yaxis_title='Nombre moyen de vélos',
    template='plotly_white',
    height=500
)

# Afficher le graphique
fig.show()

# Sauvegarder le graphique dans un fichier HTML
fig.write_html("docs/Diagramme/Diagramme_mois_2023.html")
