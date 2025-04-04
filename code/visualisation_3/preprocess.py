import pandas as pd
import os

def load_csv(filename):
    path = os.path.join("data", filename)
    return pd.read_csv(path)

def preprocess_data(df):
    df = df[(df['Year'] >= 1945) & (df['Year'] <= 2020)].copy()

    city_country_map = {
        "London": "United Kingdom", "Helsinki": "Finland", "Melbourne": "Australia",
        "Rome": "Italy", "Tokyo": "Japan", "Mexico City": "Mexico",
        "Munich": "Germany", "Montreal": "Canada", "Moscow": "Russia",
        "Los Angeles": "United States", "Seoul": "South Korea", "Barcelona": "Spain",
        "Atlanta": "United States", "Sydney": "Australia", "Athens": "Greece",
        "Beijing": "China", "Rio de Janeiro": "Brazil",
        "St. Moritz": "Switzerland", "Oslo": "Norway", "Cortina d'Ampezzo": "Italy",
        "Squaw Valley": "United States", "Innsbruck": "Austria", "Grenoble": "France",
        "Sapporo": "Japan", "Lake Placid": "United States", "Sarajevo": "Bosnia and Herzegovina",
        "Calgary": "Canada", "Albertville": "France", "Lillehammer": "Norway",
        "Nagano": "Japan", "Salt Lake City": "United States", "Turin": "Italy",
        "Vancouver": "Canada", "Sochi": "Russia", "Pyeongchang": "South Korea"
    }

    df['HostCountry'] = df['City'].map(city_country_map)
    df['IsHost'] = df['Team'] == df['HostCountry']
    df['HasMedal'] = df['Medal'].notna()
    df['Period'] = df['Year'].apply(lambda y: "1945-1991" if y <= 1991 else "1992-2020")
    df['Edition'] = df['Year'].astype(str) + "_" + df['Season']

    # Identifier nombre d’éditions uniques par groupe
    editions = df[['Team', 'Period', 'IsHost', 'Edition']].drop_duplicates()
    edition_counts = editions.groupby(['Team', 'Period', 'IsHost']).size().reset_index(name='NumEditions')

    # Nombre total d’athlètes
    athletes = df.groupby(['Team', 'Period', 'IsHost'])['Name'].nunique().reset_index(name='NumAthletes')

    # Nombre total de médailles
    medals = df[df['HasMedal']].groupby(['Team', 'Period', 'IsHost'])['Medal'].count().reset_index(name='NumMedals')

    # Merge & calculs
    summary = pd.merge(athletes, medals, on=['Team', 'Period', 'IsHost'], how='left')
    summary = pd.merge(summary, edition_counts, on=['Team', 'Period', 'IsHost'], how='left')
    summary['NumMedals'] = summary['NumMedals'].fillna(0)

    summary['AthletesPerEdition'] = summary['NumAthletes'] / summary['NumEditions']
    summary['MedalsPerEdition'] = summary['NumMedals'] / summary['NumEditions']
    summary['Ratio'] = summary['MedalsPerEdition'] / summary['AthletesPerEdition']

    # Pivot pour visualisation
    pivot = summary.pivot_table(
        index=['Team', 'Period'],
        columns='IsHost',
        values=['AthletesPerEdition', 'MedalsPerEdition', 'Ratio']
    )

    pivot.columns = [
        'Athletes_Away', 'Athletes_Host',
        'Medals_Away', 'Medals_Host',
        'Ratio_Away', 'Ratio_Host'
    ]

    pivot = pivot.reset_index()

    # Arrondir les athlètes et médailles à 0
    for col in ['Athletes_Away', 'Athletes_Host', 'Medals_Away', 'Medals_Host']:
        pivot[col] = pivot[col].round(0)

    # Arrondir le ratio à 2 décimales
    pivot['Ratio_Away'] = pivot['Ratio_Away'].round(2)
    pivot['Ratio_Host'] = pivot['Ratio_Host'].round(2)

    return pivot

