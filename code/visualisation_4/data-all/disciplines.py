# create_disciplines_from_top10.py
import pandas as pd
import os

def extract_disciplines_from_top10(athletes_file, output_file):
    """
    Lit le fichier CSV des top10 athlètes pour une saison (summer ou winter),
    extrait les disciplines uniques mentionnées dans la colonne 'discipline'
    et enregistre le résultat dans un nouveau fichier CSV.
    
    Le CSV généré contient :
      - discipline : le nom de la discipline
      - count : le nombre d'apparitions dans le top10 des athlètes (optionnel)
    """
    # Lire le CSV des top10 athlètes
    df = pd.read_csv(athletes_file)
    # Comptage du nombre d'apparitions pour chaque discipline
    discipline_counts = df['discipline'].value_counts().reset_index()
    discipline_counts.columns = ['discipline', 'count']
    
    # Sauvegarde du résultat
    discipline_counts.to_csv(output_file, index=False)
    print(f"Fichier créé : {output_file}")

if __name__ == "__main__":
    # Traitement pour la saison summer
    summer_athletes_csv = os.path.join("top10_athletes_summer.csv")
    summer_output_csv = "disciplines_summer.csv"
    extract_disciplines_from_top10(summer_athletes_csv, summer_output_csv)
    
    # Traitement pour la saison winter
    winter_athletes_csv = os.path.join("top10_athletes_winter.csv")
    winter_output_csv = "disciplines_winter.csv"
    extract_disciplines_from_top10(winter_athletes_csv, winter_output_csv)
