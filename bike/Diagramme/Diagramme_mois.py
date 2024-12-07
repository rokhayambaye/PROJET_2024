import pandas as pd
import plotly.graph_objects as go

# Charger les données
url_fichier = "https://drive.google.com/uc?id=1yJUkkGiobznF50tQaKwbM4a2bfiEVmRy"
Donnees_montpellier = pd.read_csv(url_fichier, sep=';')  # Ajouter le séparateur correct si nécessaire

# Convertir la colonne 'date' en format datetime
Donnees_montpellier['date'] = pd.to_datetime(Donnees_montpellier['date'])

# Ajouter une colonne pour le mois (1 = Janvier, 12 = Décembre)
Donnees_montpellier['month'] = Donnees_montpellier['date'].dt.month
mois = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

# Calculer le nombres de vélos par mois
moyenne_par_mois = Donnees_montpellier.groupby('month')['intensity'].sum()

# Créer un graphique interactif avec Plotly
fig = go.Figure()

# Barres du nombres de vélos par mois
fig.add_trace(go.Bar(
    x=mois,
    y=moyenne_par_mois,
    name='Nombres de Vélos',
    marker_color='green'
))

# Mise en page 
fig.update_layout(
    title='Nombres de vélos par mois (2023)',
    xaxis_title='Mois',
    yaxis_title='Nombres de Vélos (en millions)',
    template='plotly_white',
    height=500
)

# Afficher le graphique
fig.show()

# Sauvegarder le graphique dans un fichier HTML
fig.write_html("docs/Diagramme/Diagramme_Mois_2023.html")
