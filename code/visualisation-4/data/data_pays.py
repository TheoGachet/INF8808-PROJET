# csv_country_medals_season.py
import pandas as pd
import os

def create_country_medals_csv_by_season():
    """
    Crée deux fichiers CSV à partir de all_athlete_games.csv :
      - country_medals_summer.csv pour les Jeux d'été,
      - country_medals_winter.csv pour les Jeux d'hiver.
      
    Chaque CSV contient les colonnes :
      - pays (colonne 'Team')
      - or      : nombre de médailles d'or
      - argent  : nombre de médailles d'argent
      - bronze  : nombre de médailles de bronze
      - total_medals : total de médailles remportées
      - score   : score calculé (or*3 + argent*2 + bronze*1)
      
    Seules les lignes où une médaille a été remportée sont prises en compte.
    """
    source_path = os.path.join("all_athlete_games.csv")
    df = pd.read_csv(source_path)

    # Filtrer uniquement les lignes où une médaille est présente
    df = df[df['Medal'].notnull() & (df['Medal'] != "")]

    for season in ['Summer', 'Winter']:
        # Filtrer pour la saison (Jeux d'été ou Jeux d'hiver)
        df_season = df[df['Season'] == season]

        # Grouper par pays (Team) et type de médaille, et compter
        medal_counts = df_season.groupby(['Team', 'Medal']).size().unstack(fill_value=0)

        # S'assurer que les colonnes "Gold", "Silver" et "Bronze" sont présentes
        for medal in ['Gold', 'Silver', 'Bronze']:
            if medal not in medal_counts.columns:
                medal_counts[medal] = 0

        # Réorganiser et renommer les colonnes
        medal_counts = medal_counts[['Gold', 'Silver', 'Bronze']]
        medal_counts = medal_counts.rename(columns={'Gold': 'or', 'Silver': 'argent', 'Bronze': 'bronze'})

        # Calculer le total des médailles et le score
        medal_counts['total_medals'] = medal_counts['or'] + medal_counts['argent'] + medal_counts['bronze']
        medal_counts['score'] = medal_counts['or'] * 3 + medal_counts['argent'] * 2 + medal_counts['bronze'] * 1

        # Réinitialiser l'index pour avoir une colonne 'pays'
        medal_counts = medal_counts.reset_index().rename(columns={'Team': 'pays'})

        # Trier par score décroissant
        medal_counts = medal_counts.sort_values('score', ascending=False)

        # Définir le chemin de sortie selon la saison
        dest_filename = f"pays_{season.lower()}.csv"
        dest_path = os.path.join(dest_filename)
        medal_counts.to_csv(dest_path, index=False)
        print(f"Fichier créé : {dest_path}")

if __name__ == "__main__":
    create_country_medals_csv_by_season()
