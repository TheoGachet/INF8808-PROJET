# csv.py
import pandas as pd
import os

def split_name(full_name):
    """
    Sépare un nom complet en prénom et nom.
    On considère que le premier mot est le prénom et le reste constitue le nom.
    """
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
      - athletes_ete.csv (pour la saison été)
      - athletes_hiver.csv (pour la saison hiver)
      
    Le CSV généré contient les colonnes :
      - noms
      - prénoms
      - ID (correspond au plus petit Entry ID pour l'athlète dans la discipline et la saison donnée)
      - pays (Team)
      - discipline (Sport)
      - année (la première année de participation dans la discipline pour la saison)
      - médaille (nombre total de médailles remportées dans la discipline, toutes médailles confondues)
      - saison (pour distinguer été et hiver)
      
    Chaque athlète apparaît une seule fois par combinaison discipline/saison.
    Seules les participations ayant une médaille (non vide) sont prises en compte.
    """
    # Définir les chemins d'accès
    source_path = os.path.join("all_athlete_games.csv")
    
    # Charger le fichier source
    df = pd.read_csv(source_path)
    
    # Garder uniquement les lignes où une médaille est remportée
    df = df[df['Medal'].notnull() & (df['Medal'] != "")]
    
    # Regrouper par athlète, par saison et par discipline
    grouped = df.groupby(['Name', 'Season', 'Sport'])
    agg_df = grouped.agg({
        'Entry ID': 'min',
        'Team': 'first',
        'Year': 'min',
        'Medal': 'count'
    }).reset_index()
    
    # Renommer les colonnes pour correspondre à la demande
    agg_df = agg_df.rename(columns={
        'Name': 'nom',
        'Entry ID': 'ID',
        'Team': 'pays',
        'Sport': 'discipline',
        'Year': 'année',
        'Medal': 'médaille',
        'Season': 'saison'
    })
    
    # Réorganiser les colonnes
    agg_df = agg_df[['nom', 'ID', 'pays', 'discipline', 'année', 'médaille', 'saison']]
    
    # Séparer en deux DataFrames selon la saison
    # On vérifie si la saison est "été" ou "Summer" pour l'été
    # et "hiver" ou "Winter" pour l'hiver.
    df_ete = agg_df[agg_df['saison'].isin(['été', 'Summer'])]
    df_hiver = agg_df[agg_df['saison'].isin(['hiver', 'Winter'])]
    
    # Sauvegarder les résultats dans deux fichiers CSV distincts
    df_ete.to_csv("athletes_summer.csv", index=False)
    df_hiver.to_csv("athletes_winter.csv", index=False)
    print("Fichiers créés : athletes_ete.csv et athletes_hiver.csv")

if __name__ == "__main__":
    create_athletes_csv()
