import pandas as pd
import os

def split_name(full_name):
    parts = full_name.split()
    if len(parts) > 1:
        prenom = parts[0]
        nom = " ".join(parts[1:])
    else:
        prenom = full_name
        nom = ""
    return prenom, nom

def create_athletes_csv():
    """
    Crée deux fichiers CSV à partir de all_athlete_games.csv :
      - athletes_summer.csv pour la saison été
      - athletes_winter.csv pour la saison hiver
      
    Le CSV généré contient les colonnes :
      - nom
      - ID (le plus petit Entry ID pour l'athlète dans la discipline et la saison donnée)
      - pays (Team)
      - discipline (Sport)
      - année (la première année de participation dans la discipline pour la saison)
      - médaille (nombre total de médailles remportées)
      - saison
    Seules les participations avec une médaille et avec l'année >= 1992 sont prises en compte.
    """
    source_path = os.path.join("all_athlete_games.csv")
    df = pd.read_csv(source_path)
    
    # Filtrer uniquement les lignes avec une médaille
    df = df[df['Medal'].notnull() & (df['Medal'] != "")]
    # Filtrer sur l'année
    if "Year" in df.columns:
        df = df[df['Year'] >= 1992]
    elif "année" in df.columns:
        df = df[df['année'] >= 1992]
    
    # Regrouper par athlète, saison et discipline
    grouped = df.groupby(['Name', 'Season', 'Sport'])
    agg_df = grouped.agg({
        'Entry ID': 'min',
        'Team': 'first',
        'Year': 'min',
        'Medal': 'count'
    }).reset_index()
    
    agg_df = agg_df.rename(columns={
        'Name': 'nom',
        'Entry ID': 'ID',
        'Team': 'pays',
        'Sport': 'discipline',
        'Year': 'année',
        'Medal': 'médaille',
        'Season': 'saison'
    })
    
    agg_df = agg_df[['nom', 'ID', 'pays', 'discipline', 'année', 'médaille', 'saison']]
    
    df_ete = agg_df[agg_df['saison'].isin(['été', 'Summer'])]
    df_hiver = agg_df[agg_df['saison'].isin(['hiver', 'Winter'])]
    
    df_ete.to_csv("athletes_summer.csv", index=False)
    df_hiver.to_csv("athletes_winter.csv", index=False)
    print("Fichiers créés : athletes_summer.csv et athletes_winter.csv")

if __name__ == "__main__":
    create_athletes_csv()
