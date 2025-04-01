import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import hover_template as hover
import os

# Charger le fichier CSV contenant les codes et noms des pays
path = os.path.join("data", 'Countries_codes_names.csv')
country_codes = pd.read_csv(path, sep=';')


def create_multiple_heatmaps(data):
    sports = list(data.keys())  # Liste des sports
    num_sports = len(sports)  # Nombre total de sports

    # Définition du nombre de colonnes et lignes pour les subplots
    cols = 4  # Nombre de colonnes (modifiable)
    rows = 4  # Nombre de lignes (modifiable)

    # Création de la figure avec sous-graphiques
    fig = make_subplots(
        rows = rows,
        cols = cols,
        subplot_titles = sports,  # Titres des sous-graphiques
        horizontal_spacing = 0.15,
        vertical_spacing = 0.10,
    )

    # Parcours de chaque sport pour créer les heatmaps
    for i, sport in enumerate(sports):
        if sport == "Host_Countries":
            continue
        df = pd.DataFrame(data[sport])  # Convertir en DataFrame

        # Position du subplot (ligne et colonne)
        row = (i // cols) + 1
        col = (i % cols) + 1

        # Calcul du total des médailles par pays (inclut "Others")
        df['Total'] = df.sum(axis=1, numeric_only=True)

        # Effectuer le tri sur tous les pays, y compris "Others"
        df = df.sort_values(by='Total', ascending=False)

        # S'assurer que "Others" est en dernier dans l'affichage
        if "Others" in df.index:
            df = pd.concat([df.drop(index="Others"), pd.DataFrame([df.loc["Others"]])])  # Déplace "Others" à la fin

        # Supprimer la colonne "Total" après tri
        df.drop(columns=['Total'], inplace=True)

        # Inverser l'index pour que le pays avec le plus de médailles soit en haut
        df = df.loc[df.index[::-1]]

        # Mapper les codes des pays aux noms complets
        country_mapping = dict(zip(country_codes['Code'], country_codes['Name']))
        y_labels = [country_mapping.get(code, code) for code in df.index]  # Générer une liste des noms complets

        heatmap = go.Heatmap(
            z = df.values,
            x = df.columns,  # Années
            y = y_labels,  # Forcer l'ordre des pays
            xgap = 5,  # Espacement horizontal entre les cases
            ygap = 5,   # Espacement vertical entre les cases
            colorscale = "Blues",
            colorbar = dict(
            x = 0.15 + (col - 1) * 0.29,  # Décale la légende à droite de chaque heatmap
            y = 0.91 - (row - 1) * (1.10 / rows),  # Aligne la légende avec chaque subplot
            len = 0.22  # Ajuste la hauteur de la barre de couleurs
            ),
            hovertemplate=hover.get_hover_template(sport)  # Ajout des informations manquantes
        )

        # Ajout du heatmap au subplot correspondant
        fig.add_trace(heatmap, row=row, col=col)

        # Ajouter des annotations pour les pays hôtes
        for year in df.columns:
            if year in data["Host_Countries"]:
                host_country = data["Host_Countries"][year]
                if host_country in df.index:
                    y_index = df.index.get_loc(host_country)

                    # Définir la taille du rectangle
                    size_x = 1.8
                    size_y = 0.5
                    
                    fig.add_shape(
                        type="rect",
                        x0=int(year) - size_x,  # Début de l'année avec une marge
                        x1=int(year) + size_x,  # Fin de l'année avec une marge
                        y0=y_index - size_y,  # Début du pays avec une marge
                        y1=y_index + size_y,  # Fin du pays avec une marge
                        xref=f"x{i+1}",
                        yref=f"y{i+1}",
                        line=dict(color="red", width=2),
                    )

    # Ajouter une légende pour le rectangle rouge en utilisant une case fictive de la heatmap
    fig.add_trace(
        go.Scatter(
            x=[None],  # Valeur fictive pour la légende
            y=[None],
            mode="markers",
            marker=dict(
                size=12,
                color="red",
                symbol="square-open"  # Carré non rempli
            ),
            name="Pays organisateur"
        )
    )

    # Mise à jour de la position de la légende pour qu'elle soit affichée en haut des heatmaps
    fig.update_layout(
        legend=dict(
            orientation="h",  # Légende horizontale
            yanchor="bottom",
            y=1.05,  # Position au-dessus des heatmaps
            xanchor="center",
            x=0.5  # Centrer la légende
        )
    )

    # Mise à jour de la mise en page globale
    fig.update_layout(
        height = rows * 370,  # Ajustement de la hauteur en fonction du nombre de lignes
        width = cols * 370,  # Augmentation de la largeur pour bien afficher les légendes
        showlegend = True,  # Activer la légende globale
    )

    return fig