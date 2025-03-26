import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def create_heatmap(data, sport="Athletics"):
    # Vérifier si le sport existe dans le dictionnaire
    if sport not in data:
        raise ValueError(f"Le sport '{sport}' n'existe pas dans les données.")

    # Extraire les données pour le sport spécifié
    athletics_data = data[sport]

    # Convertir en DataFrame (au cas où ce n'est pas encore un DataFrame)
    athletics_df = pd.DataFrame(athletics_data)

    # Créer une heatmap avec Plotly
    fig = px.imshow(
        athletics_df,
        labels={"x": "Year", "y": "Country", "color": "Medals"},
        color_continuous_scale="Blues",
        title=f"Heatmap for {sport}"
    )

    return fig


def create_multiple_heatmaps(data):
    sports = list(data.keys())  # Liste des sports dans le dictionnaire
    num_sports = len(sports)  # Nombre total de sports

    # Définition du nombre de colonnes et lignes pour les subplots
    cols = 4  # On affiche 4 heatmaps par ligne
    rows = (num_sports // cols) + (num_sports % cols > 0)  # Calcul du nombre de lignes

    # Création de la figure avec sous-graphiques
    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=sports,  # Titres des subplots avec les noms des sports
        horizontal_spacing=0.05, vertical_spacing=0.1
    )

    # Parcours de chaque sport pour créer les heatmaps
    for i, sport in enumerate(sports):
        athletics_df = pd.DataFrame(data[sport])  # Convertir les données en DataFrame

        heatmap = go.Heatmap(
            z=athletics_df.values,
            x=athletics_df.columns,  # Années
            y=athletics_df.index,  # Pays
            colorscale="Blues",
            colorbar=dict(title="Medals")
        )

        # Ajout du heatmap au subplot correspondant
        row = (i // cols) + 1
        col = (i % cols) + 1
        fig.add_trace(heatmap, row=row, col=col)

    # Mise à jour de la mise en page globale
    fig.update_layout(
        title_text="Small Multiple: Heatmaps for All Sports",
        height=rows * 400,  # Ajuster la hauteur en fonction du nombre de lignes
        width=cols * 400,  # Ajuster la largeur
        showlegend=False
    )

    return fig