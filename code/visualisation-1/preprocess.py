# j'ai utilisé le TP3 comme base pour ajouter une visualisation dessusc

import pandas as pd
import os

def load_csv(filename):
    """
    Charge un fichier CSV depuis le dossier 'data'.
    """
    path = os.path.join("data", filename)
    return pd.read_csv(path)

data = load_csv("all_athlete_games.csv")

summer_sports = [
    "Athletics", "Rowing", "Badminton", "Basketball", "Boxing", "Canoeing", 
    "Cycling", "Equestrian", "Fencing", "Foot", "Artistic Gymnastics", 
    "Handball", "Judo", "Wrestling", "Swimming", "Sailing"
]

winter_sports = [
    "Alpine Skiing", "Alpinism", "Biathlon", "Bobsleigh", "Cross Country Skiing", "Curling", 
    "Figure Skating", "Ice Hockey", "Luge", "Nordic Combined", "Ski Jumping", "Skeleton", "Ski", "Snowboarding"
]

summer_data = data[data['Sport'].isin(summer_sports)]
summer_years = summer_data[(summer_data['Year'] >= 1991) & (summer_data['Year'] <= 2020)]
medal_counts_summer = summer_years.groupby('Sport')['Medal'].count()
print(medal_counts_summer)