import pandas as pd
import os

def load_csv(filename):
    """
    Charge un fichier CSV depuis le dossier 'data'.
    """
    path = os.path.join("data", filename)
    return pd.read_csv(path)

def preprocess_data(df, season=None):
    """
    Prépare les données pour les lollipops charts.
    """
    # 1. Filtrer les données pour la période 1945-2020 et éventuellement la saison
    df = df[(df['Year'] >= 1945) & (df['Year'] <= 2020)].copy()
    if season:
        df = df[df['Season'] == season].copy()

    # 2. Mapping des villes hôtes vers pays hôtes
    city_country_map = {
        # Été
        "London": "United Kingdom", "Helsinki": "Finland", "Melbourne": "Australia",
        "Rome": "Italy", "Tokyo": "Japan", "Mexico City": "Mexico",
        "Munich": "Germany", "Montreal": "Canada", "Moscow": "Russia",
        "Los Angeles": "United States", "Seoul": "South Korea", "Barcelona": "Spain",
        "Atlanta": "United States", "Sydney": "Australia", "Athens": "Greece",
        "Beijing": "China", "Rio de Janeiro": "Brazil",
        # Hiver
        "St. Moritz": "Switzerland", "Oslo": "Norway", "Cortina d'Ampezzo": "Italy",
        "Squaw Valley": "United States", "Innsbruck": "Austria", "Grenoble": "France",
        "Sapporo": "Japan", "Lake Placid": "United States", "Sarajevo": "Bosnia and Herzegovina",
        "Calgary": "Canada", "Albertville": "France", "Lillehammer": "Norway",
        "Nagano": "Japan", "Salt Lake City": "United States", "Turin": "Italy",
        "Vancouver": "Canada", "Sochi": "Russia", "Pyeongchang": "South Korea"
    }

    # 3. Ajouter colonnes nécessaires
    df['HostCountry'] = df['City'].map(city_country_map)
    df['IsHost'] = df['Team'] == df['HostCountry']
    df['HasMedal'] = df['Medal'].notna()

    def get_period(year):
        return "1945-1991" if year <= 1991 else "1992-2020"

    df['Period'] = df['Year'].apply(get_period)

    # 4. Moyennes d’athlètes par pays / période / IsHost (nombre moyen par édition)
    athlete_counts = (
        df.groupby(['Team', 'Year', 'Period', 'IsHost'])['Name']
        .nunique()
        .reset_index(name='NumAthletesPerEdition')
    )
    athletes_per_group = (
        athlete_counts.groupby(['Team', 'Period', 'IsHost'])['NumAthletesPerEdition']
        .mean()
        .reset_index(name='NumAthletes')
    )

    # 5. Moyennes de médailles par pays / période / IsHost (nombre moyen par édition)
    medal_counts = (
        df[df['HasMedal']]
        .groupby(['Team', 'Year', 'Period', 'IsHost'])['Medal']
        .count()
        .reset_index(name='NumMedalsPerEdition')
    )
    medals_per_group = (
        medal_counts.groupby(['Team', 'Period', 'IsHost'])['NumMedalsPerEdition']
        .mean()
        .reset_index(name='NumMedals')
    )

    # 6. Jointure + Ratio
    summary = pd.merge(athletes_per_group, medals_per_group,
                       on=['Team', 'Period', 'IsHost'], how='left')
    summary['NumMedals'] = summary['NumMedals'].fillna(0)
    summary['Ratio'] = summary['NumMedals'] / summary['NumAthletes']

    # Arrondi à 0 décimale sauf Ratio à 2 décimales
    summary['NumAthletes'] = summary['NumAthletes'].round(0)
    summary['NumMedals'] = summary['NumMedals'].round(0)
    summary['Ratio'] = summary['Ratio'].round(2)

    # 7. Pivot pour structure finale
    pivot = summary.pivot_table(
        index=['Team', 'Period'],
        columns='IsHost',
        values=['NumAthletes', 'NumMedals', 'Ratio']
    )

    pivot.columns = [
        'Athletes_Away', 'Athletes_Host',
        'Medals_Away', 'Medals_Host',
        'Ratio_Away', 'Ratio_Host'
    ]

    pivot = pivot.reset_index()

    return pivot

