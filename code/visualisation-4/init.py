from preprocess import load_csv
from dash import html

def get_output(season, discipline):
    """
    Retourne une représentation HTML décrivant, pour le type de Jeux (season)
    et la discipline sélectionnée,
    le top 10 des pays (chargés depuis top10_pays_{season.lower()}.csv)
    et, pour chacun, la liste des athlètes (chargés depuis top10_athletes_{season.lower()}.csv)
    avec leur nombre de médailles et leur discipline indiquée.
    Les athlètes dont la discipline correspond (comparaison insensible à la casse)
    à celle sélectionnée sont affichés en rouge.
    """
    # Charger les données des pays et des athlètes
    df_pays = load_csv(f"top10_pays_{season.lower()}.csv")
    df_athletes = load_csv(f"top10_athletes_{season.lower()}.csv")
    
    # Pour df_pays, utiliser "pays" si présent, sinon "NOC"
    noc_col_pays = "pays" if "pays" in df_pays.columns else "NOC"
    
    # Pour df_athletes, on utilise directement les noms tels qu'ils apparaissent dans le CSV :
    # - "pays" pour le code pays,
    # - "nom" pour le nom de l'athlète,
    # - "discipline" pour la discipline,
    # - "médaille" pour le nombre de médailles.
    noc_col = "pays"
    name_col = "nom"
    medal_col = "médaille"
    disc_col = "discipline"
    
    output_components = []
    output_components.append(html.H2(f"Visualisation pour {season} - Discipline: {discipline}"))
    output_components.append(html.P("Top 10 pays par points cumulés (1992-2020):"))
    
    # Pour chaque pays du fichier top10_pays, afficher les athlètes correspondants
    for _, row in df_pays.iterrows():
        country = row[noc_col_pays]
        # On essaie de récupérer le score (Points ou points) dans le CSV des pays
        points = row.get("score", row.get("score", ""))
        output_components.append(html.H3(f"Pays: {country} - Points: {points}"))
        
        # Filtrer les athlètes pour ce pays
        df_country = df_athletes[df_athletes[noc_col] == country]
        if df_country.empty:
            output_components.append(html.P("  Aucun athlète trouvé."))
        else:
            for _, arow in df_country.iterrows():
                name = arow.get(name_col, "Inconnu")
                athlete_discipline = arow.get(disc_col, "Non renseigné")
                medal_count = arow.get(medal_col, 0)
                text = f"{name} - {athlete_discipline} ({medal_count} médailles)"
                # Comparaison insensible à la casse pour la discipline
                if athlete_discipline.lower() == discipline.lower():
                    output_components.append(html.P(html.Span(text, style={'color': 'red'})))
                else:
                    output_components.append(html.P(text))
    return output_components
