import pandas as pd
import plotly.graph_objects as go

# Charger les données
url_fichier = "https://drive.google.com/uc?id=1yJUkkGiobznF50tQaKwbM4a2bfiEVmRy"
Donnees_montpellier = pd.read_csv(url_fichier, sep=';')  # Ajouter le séparateur correct si nécessaire

# Convertir la colonne 'date' en format datetime
Donnees_montpellier['date'] = pd.to_datetime(Donnees_montpellier['date'])

# Regrouper par date et calculer la somme des intensités
flux_global = Donnees_montpellier.groupby('date')['intensity'].sum()


# Ajouter une colonne pour le jour de la semaine (0 = Lundi, 6 = Dimanche)
Donnees_montpellier['weekday'] = Donnees_montpellier['date'].dt.dayofweek

# Calculer la moyenne des flux par jour de la semaine
moyenne_par_jour = Donnees_montpellier.groupby('weekday')['intensity'].mean()
jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

fig = go.Figure()

fig.add_trace(go.Bar(
    x=jours_semaine,
    y=moyenne_par_jour,
    name='Moyenne des flux',
    marker_color='green'
))

# Ajouter des détails au graphique
fig.update_layout(
    title='Nombre de vélos moyen par jour de la semaine (2023)',
    xaxis_title='Jour de la semaine',
    yaxis_title='Nombre moyen de vélos',
    template='plotly_white',
    height=500
)

# Afficher le graphique
fig.show()
fig.write_html("docs/Diagramme/Diagramme_Semaine_2023.html")
