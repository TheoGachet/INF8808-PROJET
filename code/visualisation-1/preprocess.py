# j'ai utilisé le TP3 comme base pour ajouter une visualisation dessus

import pandas as pd
import matplotlib.pyplot as plt
import os


def load_csv(filename):
    """
    Charge un fichier CSV depuis le dossier 'data'.
    """
    path = os.path.join("data", filename)
    return pd.read_csv(path)

data = load_csv("all_athlete_games.csv")

summer_sports = [
    "Artistic Gymnastics","Athletics", "Badminton", "Basketball", "Boxing",
    "Canoeing", "Cycling", "Equestrian", "Fencing", "Foot", 
    "Handball", "Judo", "Rowing", "Sailing", "Swimming", "Wrestling"
]

summer_countries = ['FRA', 'USA', 'CHN', 'RUS', 'GER', 'GBR', 'JPN', 'AUS', 'ITA', 'CAN']

winter_sports = [
    "Alpine Skiing", "Alpinism", "Biathlon", "Bobsleigh", "Cross Country Skiing", "Curling", 
    "Figure Skating", "Ice Hockey", "Luge", "Nordic Combined", "Ski Jumping", "Skeleton", "Ski", "Snowboarding"
]

def convert_data():

    summer_medal_counts = {}

    filtered_data = data[(data['Year'] >= 1991) & (data['Year'] <= 2020)]

    for sport in summer_sports:
        sport_data = filtered_data[filtered_data['Sport'] == sport]
        if not sport_data.empty:
            # Group by NOC and Year, then count medals
            medals_by_country_year = sport_data.groupby(['NOC', 'Year'])['Medal'].count().unstack(fill_value=0)
            sorted_medals = medals_by_country_year.sum(axis=1).sort_values(ascending=False)
            top_countries = sorted_medals.head(10).index  # Get top 10 countries
            top_countries_data = medals_by_country_year.loc[top_countries]

            # Sum medals for countries outside the top 10
            others_data = medals_by_country_year.drop(top_countries).sum()
            top_countries_data.loc['Others'] = others_data

            summer_medal_counts[sport] = top_countries_data

    # for sport, top_countries in summer_medal_counts.items():
    #     print(f"Top 10 countries (and Others) for {sport}:")
    #     print(top_countries_data)
    #     print()

    return summer_medal_counts