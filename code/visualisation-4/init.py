import circlify
import plotly.graph_objects as go
from preprocess import load_csv
from dash import html, dcc
import math
import pandas as pd

def split_name(full_name):
    """
    Sépare un nom complet en prénom et nom.
    On considère que le premier mot est le prénom et le reste constitue le nom.
    """
    parts = full_name.split()
    if len(parts) >= 2:
        first_name = parts[0]
        last_name = " ".join(parts[1:])
    else:
        first_name = full_name
        last_name = ""
    return first_name, last_name

def get_output(season, discipline):
    """
    Retourne une représentation HTML combinant :
      - Pour chaque pays (du fichier top10_pays_{season.lower()}.csv) :
          • Un graphique "packed circle chart" où chaque cercle représente un athlète,
            la taille du cercle est proportionnelle au nombre de médailles obtenues,
            et le cercle est coloré en rouge si l’athlète exerce la discipline sélectionnée (insensible à la casse),
            sinon en bleu.
          • Sur le graphique, seule l'annotation du nom de famille (extrait de "nom_norm") est affichée.
          • En hover, une bulle affiche :
                Nom : [nom de famille]<br>
                Prénom : [prénom]<br>
                Pays : [pays]<br>
                Discipline : [discipline]<br>
                Médailles d'or : [nombre]<br>
                Médailles d'argent : [nombre]<br>
                Médailles de bronze : [nombre]
      - Les graphiques sont affichés côte à côte avec trois par ligne.
    """
    # Charger les données
    df_pays = load_csv(f"top10_pays_{season.lower()}.csv")
    df_athletes_top = load_csv(f"top10_athletes_{season.lower()}.csv")
    # Charger le CSV complet pour le calcul détaillé des médailles
    all_athletes = load_csv("all_athlete_games.csv")
    # Filtrer sur l'année >= 1992 (supposons que la colonne s'appelle "Year" ou "année")
    if "Year" in all_athletes.columns:
        all_athletes = all_athletes[all_athletes["Year"] >= 1992]
    elif "année" in all_athletes.columns:
        all_athletes = all_athletes[all_athletes["année"] >= 1992]
    
    # Colonnes utilisées
    country_col = "pays" if "pays" in df_pays.columns else "NOC"
    athlete_country_col = "pays"
    # On utilise "nom_norm" pour extraire le prénom et le nom
    name_col = "nom_norm"
    medal_col = "médaille"
    disc_col = "discipline"
    
    output_components = []
    output_components.append(html.H2(f"Visualisation pour {season} - Discipline sélectionnée : {discipline}"))
    output_components.append(html.P("Top 10 pays par score :"))
    
    # Accumulateur de composants pour chaque pays
    country_components = []
    
    for _, row in df_pays.iterrows():
        country = row[country_col]
        score = row.get("score", row.get("Score", ""))
        header = html.H3(f"Pays : {country} - Score : {score}")
        
        # Filtrer les athlètes pour ce pays dans le CSV top10
        df_country = df_athletes_top[df_athletes_top[athlete_country_col] == country]
        if df_country.empty:
            comp = html.Div([header, html.P("Aucun athlète trouvé.")],
                            style={'marginBottom': '40px', 'border': '1px solid #ccc', 'padding': '10px'})
            country_components.append(comp)
            continue
        
        # Construire la liste des athlètes en utilisant "nom_norm"
        athletes = []
        for _, arow in df_country.iterrows():
            try:
                medals = float(arow.get(medal_col, 0))
            except:
                medals = 0.0
            athletes.append({
                "name": arow.get(name_col, "Inconnu"),
                "discipline": arow.get(disc_col, "Non renseigné"),
                "medals": medals
            })
        
        # Trier les athlètes par nombre de médailles décroissant
        athletes = sorted(athletes, key=lambda x: x["medals"], reverse=True)
        medal_values = [ath["medals"] for ath in athletes]
        
        # Calculer la disposition des cercles avec circlify
        circles = circlify.circlify(
            medal_values,
            show_enclosure=False,
            target_enclosure=circlify.Circle(x=0, y=0, r=1)
        )
        circles = sorted(circles, key=lambda c: c.r, reverse=True)
        
        # Création de la figure Plotly pour ce pays avec dimensions agrandies
        TAILLE = 450
        fig = go.Figure()
        fig.update_xaxes(range=[-1.1, 1.1], showgrid=False, zeroline=False, visible=False)
        fig.update_yaxes(range=[-1.1, 1.1], showgrid=False, zeroline=False, visible=False)
        
        # Préparer les listes pour le trace scatter invisible qui gère le hover
        x_scatter, y_scatter, hover_text_list, marker_sizes, marker_color_list = [], [], [], [], []
        for ath, circle in zip(athletes, circles):
            first_name, last_name = split_name(ath["name"])
            color = "red" if ath["discipline"].lower() == discipline.lower() else "blue"
            x, y, r = circle.x, circle.y, circle.r
            # Ajouter le cercle via add_shape
            fig.add_shape(
                type="circle",
                xref="x", yref="y",
                x0=x - r, y0=y - r, x1=x + r, y1=y + r,
                line_color=color,
                fillcolor=color,
                opacity=0.5
            )
            # Annotation affichant uniquement le nom de famille sur le cercle
            fig.add_annotation(
                x=x, y=y,
                text=last_name,
                showarrow=False,
                font=dict(color="white", size=10)
            )
            
            # Calculer la répartition détaillée des médailles pour cet athlète à partir de all_athletes
            df_ath = all_athletes[
                (all_athletes["Name"] == ath["name"]) &
                (all_athletes["Season"] == season) &
                (all_athletes["Sport"] == ath["discipline"])
            ]
            gold = int((df_ath["Medal"] == "Gold").sum())
            silver = int((df_ath["Medal"] == "Silver").sum())
            bronze = int((df_ath["Medal"] == "Bronze").sum())
            
            # Préparer le texte du hover en ajoutant la discipline
            hover_text = (
                f"Nom : {last_name}<br>"
                f"Prénom : {first_name}<br>"
                f"Pays : {country}<br>"
                f"Discipline : {ath['discipline']}<br>"
                f"Médailles d'or : {gold}<br>"
                f"Médailles d'argent : {silver}<br>"
                f"Médailles de bronze : {bronze}"
            )
            x_scatter.append(x)
            y_scatter.append(y)
            hover_text_list.append(hover_text)
            marker_sizes.append(r * 200)  # ajustez l'échelle si besoin
            marker_color_list.append(color)
        
        # Ajouter le trace scatter invisible pour le hover
        fig.add_trace(go.Scatter(
            x=x_scatter,
            y=y_scatter,
            mode='markers',
            marker=dict(
                size=marker_sizes,
                color=marker_color_list,
                opacity=0
            ),
            hoverinfo='text',
            hovertext=hover_text_list,
            showlegend=False
        ))
        
        fig.update_layout(
            width=TAILLE, height=TAILLE,
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor="white"
        )
        
        graph_component = dcc.Graph(figure=fig)
        comp = html.Div([header, graph_component],
                        style={'marginBottom': '40px', 'border': '1px solid #ccc', 'padding': '10px', 'width': f'{TAILLE}px'})
        country_components.append(comp)
    
    # Regrouper en lignes (3 par ligne maximum)
    rows = []
    for i in range(0, len(country_components), 3):
        row = html.Div(country_components[i:i+3],
                       style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-around'})
        rows.append(row)
    
    output_components = [
        html.H2(f"Visualisation pour {season} - Discipline sélectionnée : {discipline}"),
        html.P("Top 10 pays par score :"),
        html.Div(rows)
    ]
    
    return output_components
