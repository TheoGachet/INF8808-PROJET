import pandas as pd
import os

def get_top_countries(file_path):
    """
    Lit le fichier CSV contenant les top 10 pays (top10_pays_summer.csv ou top10_pays_winter.csv)
    et renvoie une liste des pays présents dans la colonne 'pays'.
    """
    df = pd.read_csv(file_path)
    return df['pays'].tolist()

def get_medal_breakdown():
    """
    Lit le fichier all_athlete_games.csv, filtre sur l'année >= 1992 et les lignes où une médaille est remportée,
    puis groupe par Name, Season et Sport pour compter le nombre de Gold, Silver et Bronze.
    Retourne un DataFrame avec les colonnes :
       - Name, Season, Sport, gold, silver, bronze
    """
    df = pd.read_csv("all_athlete_games.csv")
    # Filtrer sur l'année >= 1992
    if "Year" in df.columns:
        df = df[df["Year"] >= 1992]
    elif "année" in df.columns:
        df = df[df["année"] >= 1992]
    # Conserver uniquement les lignes où une médaille est présente
    df = df[df["Medal"].notnull() & (df["Medal"] != "")]
    # Grouper par Name, Season, Sport et compter les occurrences de chaque type de médaille
    breakdown = df.groupby(["Name", "Season", "Sport"])["Medal"].value_counts().unstack(fill_value=0).reset_index()
    # S'assurer que les colonnes Gold, Silver et Bronze existent
    for col in ["Gold", "Silver", "Bronze"]:
        if col not in breakdown.columns:
            breakdown[col] = 0
    breakdown = breakdown.rename(columns={"Gold": "gold", "Silver": "silver", "Bronze": "bronze"})
    return breakdown

def top_athletes_by_country(athletes_file, top_countries, top_athletes_per_country=10):
    """
    Pour chaque pays dans la liste top_countries,
    sélectionne la réunion de deux ensembles :
      - Les top 'top_athletes_per_country' athlètes (triés par la colonne 'médaille' décroissante),
      - Tous les athlètes ayant >= 5 médailles.
    Fusionne ensuite avec le détail des médailles (gold, silver, bronze) calculé à partir de all_athlete_games.csv.
    
    Retourne un DataFrame contenant l'ensemble des athlètes sélectionnés avec les colonnes gold, silver et bronze.
    """
    df = pd.read_csv(athletes_file)
    dfs = []
    breakdown = get_medal_breakdown()
    # Pour faciliter la fusion, on suppose que le CSV des athlètes agrégé a une colonne "nom" qui correspond à "Name" dans breakdown,
    # une colonne "saison" qui correspond à "Season" et "discipline" qui correspond à "Sport".
    for country in top_countries:
        # Sélectionner les athlètes du pays
        df_country = df[df['pays'] == country]
        if df_country.empty:
            continue
        
        # Sélectionner les top 10 athlètes par médaille (tri décroissant)
        df_top10 = df_country.sort_values(by='médaille', ascending=False).head(top_athletes_per_country)
        # Sélectionner tous les athlètes ayant >= 5 médailles
        df_above5 = df_country[df_country['médaille'] >= 5]
        # Combiner les deux ensembles et supprimer les doublons
        df_combined = pd.concat([df_top10, df_above5]).drop_duplicates()
        # Fusionner avec le breakdown sur les clés : nom vs Name, saison vs Season, discipline vs Sport
        df_merged = pd.merge(
            df_combined,
            breakdown,
            left_on=["nom", "saison", "discipline"],
            right_on=["Name", "Season", "Sport"],
            how="left"
        )
        # Remplacer les valeurs manquantes par 0 pour les médailles détaillées
        for col in ["gold", "silver", "bronze"]:
            if col in df_merged.columns:
                df_merged[col] = df_merged[col].fillna(0).astype(int)
            else:
                df_merged[col] = 0
        dfs.append(df_merged)
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()

def create_top_athletes_csv():
    """
    Crée deux fichiers CSV finaux :
      - top10_athletes_summer.csv (pour l'été)
      - top10_athletes_hiver.csv (pour l'hiver)
      
    Pour chaque saison, le script :
      1. Lit le fichier des top 10 pays (top10_pays_summer.csv ou top10_pays_winter.csv),
      2. Extrait la liste des pays,
      3. Lit le CSV des athlètes correspondant (athletes_summer.csv ou athletes_hiver.csv),
      4. Pour chaque pays, sélectionne la réunion des 10 athlètes ayant le plus haut score OU tous ceux qui ont >= 5 médailles,
      5. Fusionne avec la répartition détaillée (gold, silver, bronze),
      6. Sauvegarde le résultat dans un CSV distinct.
    """
    # Traitement pour la saison été
    top10_pays_summer_file = os.path.join("top10_pays_summer.csv")
    athletes_summer_file = os.path.join("athletes_summer.csv")
    top10_pays_summer = get_top_countries(top10_pays_summer_file)
    df_top_summer = top_athletes_by_country(athletes_summer_file, top10_pays_summer, top_athletes_per_country=10)
    output_summer = "top10_athletes_summer.csv"
    df_top_summer.to_csv(output_summer, index=False)
    print(f"Fichier créé pour l'été : {output_summer}")
    
    # Traitement pour la saison hiver
    top10_pays_winter_file = os.path.join("top10_pays_winter.csv")
    athletes_winter_file = os.path.join("athletes_winter.csv")
    top10_pays_winter = get_top_countries(top10_pays_winter_file)
    df_top_winter = top_athletes_by_country(athletes_winter_file, top10_pays_winter, top_athletes_per_country=10)
    output_winter = "top10_athletes_winter.csv"
    df_top_winter.to_csv(output_winter, index=False)
    print(f"Fichier créé pour l'hiver : {output_winter}")

if __name__ == "__main__":
    create_top_athletes_csv()
