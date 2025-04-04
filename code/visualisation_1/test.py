# j'ai utilisé le TP3 comme base pour ajouter une visualisation dessus

import preprocess as preprocess

if __name__ == "__main__":
    try:
        df = preprocess.load_csv("INF8808/INF8808-PROJET/data/all_athlete_games.csv")
        print("CSV chargé avec succès")
        print(df.head())
    except Exception as e:
        print("Erreur lors du chargement du CSV")
        print(e)
