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
    "Athletics", "Badminton", "Basketball", "Boxing",
    "Canoeing", "Cycling", "Fencing", "Football", "Gymnastics",
    "Handball", "Judo", "Rowing", "Sailing", "Swimming", "Weightlifting", "Wrestling"
]

winter_sports = [
    "Alpine Skiing", "Biathlon", "Bobsleigh", "Cross Country Skiing", "Curling", 
    "Figure Skating", "Ice Hockey", "Luge", "Nordic Combined", "Ski Jumping", "Skeleton", "Snowboarding"
]

organaizing_countries ={
    "Albertville": "FRA",
    "Amsterdam": "NED",
    "Antwerpen": "BEL",
    "Athina": "GRE",
    "Atlanta": "USA",
    "Barcelona": "ESP",
    "Beijing": "CHN",
    "Berlin": "GER",
    "Calgary": "CAN",
    "Chamonix": "FRA",
    "Cortina d'Ampezzo": "ITA",
    "Garmisch-Partenkirchen": "GER",
    "Grenoble": "FRA",
    "Helsinki": "FIN",
    "Innsbruck": "AUT",
    "Lake Placid": "USA",
    "Lillehammer": "NOR",
    "London": "GBR",
    "Los Angeles": "USA",
    "Melbourne": "AUS",
    "Mexico City": "MEX",
    "Montreal": "CAN",
    "Moskva": "RUS",
    "Munich": "GER",
    "Nagano": "JPN",
    "Oslo": "NOR",
    "Paris": "FRA",
    "Rio de Janeiro": "BRA",
    "Roma": "ITA",
    "Salt Lake City": "USA",
    "Sankt Moritz": "SUI",
    "Sapporo": "JPN",
    "Sarajevo": "BIH",
    "Seoul": "KOR",
    "Sochi": "RUS",
    "Squaw Valley": "USA",
    "St. Louis": "USA",
    "Stockholm": "SWE",
    "Sydney": "AUS",
    "Tokyo": "JPN",
    "Torino": "ITA",
    "Vancouver": "CAN"
}


def convert_data(season):

    """
    Convertit les données pour obtenir les médailles par sport et par pays.
    Filtre les données entre 1991 et 2020, puis calcule les médailles pour les
    10 meilleurs pays par sport, en regroupant les autres pays sous 'Others'.
    """

    # sports = summer_sports  # Liste des sports d'été à analyser
    # season = 'summer'  # Saison des sports à analyser

    if season == 'Summer':
        sports = summer_sports
        filtered_data = data[(data['Year'] >= 1992) & (data['Year'] <= 2020)]
    else:
        sports = winter_sports
        filtered_data = data[(data['Year'] >= 1994) & (data['Year'] <= 2020)]

    medal_counts = {}  # Dictionnaire pour stocker les médailles par sport

    # Filtrer les données pour les années entre 1991 et 2020
    # filtered_data = data[(data['Year'] >= 1992) & (data['Year'] <= 2020)]

    for sport in sports:
        # Filtrer les données pour un sport spécifique
        sport_data = filtered_data[filtered_data['Sport'] == sport]
        if not sport_data.empty:
            # Grouper par NOC (pays) et année, puis compter les médailles
            medals_by_country_year = sport_data.groupby(['NOC', 'Year'])['Medal'].count().unstack(fill_value=0)
            
            # Trier les pays par le total des médailles (somme sur toutes les années)
            sorted_medals = medals_by_country_year.sum(axis=1).sort_values(ascending=False)

            # Trier par total des médailles en ordre décroissant, puis par NOC en ordre alphabétique
            sorted_medals = sorted_medals.sort_index(ascending=True).sort_values(ascending=False, kind='mergesort')
            
            # Obtenir les 10 meilleurs pays
            top_countries = sorted_medals.head(10).index
            
            # Extraire les données pour les 10 meilleurs pays
            top_countries_data = medals_by_country_year.loc[top_countries]

            # Calculer les médailles pour les pays hors du top 10
            others_data = medals_by_country_year.drop(top_countries).sum()
            
            # Ajouter une ligne 'Others' pour les autres pays
            top_countries_data.loc['Others'] = others_data

            # Ajouter les données au dictionnaire pour le sport actuel
            medal_counts[sport] = top_countries_data

    
    # Ajouter une colonne pour le code du pays organisateur
    filtered_data['Host_Country'] = filtered_data['City'].map(organaizing_countries)

    # Créer un dictionnaire avec les années comme clés et les codes des pays organisateurs comme valeurs
    host_countries_by_year = filtered_data[filtered_data['Season'] == season][['Year', 'Host_Country']].drop_duplicates().sort_values('Year')
    host_countries_dict = dict(zip(host_countries_by_year['Year'], host_countries_by_year['Host_Country']))

    # Ajouter les données des pays organisateurs dans medal_counts
    medal_counts['Host_Countries'] = host_countries_dict
    
    return medal_counts