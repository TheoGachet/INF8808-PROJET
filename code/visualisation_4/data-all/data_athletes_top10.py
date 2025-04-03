import pandas as pd
import os

def get_top_countries(file_path):
    """
    Lit le fichier CSV contenant les top 10 pays (top10_pays_summer.csv ou top10_pays_winter.csv)
    et renvoie une liste des pays présents dans la colonne 'pays'.
    """
    df = pd.read_csv(file_path)
    return df['pays'].tolist()

def top_athletes_by_country(athletes_file, top_countries, top_athletes_per_country=10):
    """
    Pour chaque pays dans la liste top_countries,
    sélectionne la réunion de deux ensembles :
      - Les top 'top_athletes_per_country' athlètes (triés par la colonne 'médaille' décroissante),
      - Tous les athlètes ayant plus de 5 médailles.
    
    Retourne un DataFrame contenant l'ensemble des athlètes sélectionnés.
    """
    df = pd.read_csv(athletes_file)
    dfs = []
    for country in top_countries:
        # Sélectionner les athlètes du pays
        df_country = df[df['pays'] == country]
        if df_country.empty:
            continue
        
        # Sélectionner les top 10 athlètes par médaille (score décroissant)
        df_top10 = df_country.sort_values(by='médaille', ascending=False).head(top_athletes_per_country)
        # Sélectionner tous les athlètes ayant plus de 5 médailles
        df_above5 = df_country[df_country['médaille'] > 5]
        # Combiner les deux ensembles et supprimer les doublons
        df_combined = pd.concat([df_top10, df_above5]).drop_duplicates()
        dfs.append(df_combined)
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
      4. Pour chaque pays, sélectionne la réunion des 10 athlètes ayant le plus haut score OU tous ceux qui ont plus de 5 médailles,
      5. Sauvegarde le résultat dans un CSV distinct.
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
