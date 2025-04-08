import pandas as pd
import numpy as np
import os

def load_csv(filename):
    """
    Charge un fichier CSV depuis le dossier 'data'.
    """
    path = os.path.join("data", filename)

    return pd.read_csv(path)

data = load_csv("all_athlete_games.csv")


def rejet_annees(data, annee_inf, ete = True):
    """
    Rejette les lignes dont la valeur de la colonne "Year" est inférieure à `annee_inf`.
    ---
    Arguments:
        -`data`: DataFrame
        -`annee_inf`: int: Année minimale à conserver
    
    Returns:
        -`data`: DataFrame sans les lignes rejetées
    """
    data["Year"] = data["Year"].astype("Int64")

    if ete:
        data = data[data["Season"] == "Summer"]
    else:
        data = data[data["Season"] == "Winter"]


    return data[data["Year"] >= annee_inf]

def points(data):
    """
    Ajoute une colonne "Medals" et une colonne "Points" au dataframe.
    ---
    Arguments:
        -`data`: DataFrame
    
    Returns:
        -`data`: DataFrame avec les nouvelles colonnes
    """

    # Remplissage de la colonne Medals avec des 0 et 1:
    data.loc[data["Medal"].isin(["Gold", "Silver", "Bronze"]), "Medals"] = 1
    data["Medals"] = data["Medals"].fillna(0).astype(int)

    # Création de la colonne Points:
    data["Points"]=np.nan

    data.loc[data["Medal"]=="Gold", "Points"]=3
    data.loc[data["Medal"]=="Silver", "Points"]=2
    data.loc[data["Medal"]=="Bronze", "Points"]=1
    data["Points"] = data["Points"].fillna(0).astype(int)

    return data

def data_without(data):
    df_medals_count = data.groupby(["Name", "Year"])["Medals"].sum().reset_index()
    athletes_to_keep = df_medals_count[df_medals_count["Medals"] < 2]["Name"]
    data_without = data[data["Name"].isin(athletes_to_keep)]

    return data_without


def pays_points(data_with, data_without):
    """
    Retourne le nombre de points par pays et par année.
    ---
    Arguments:
        -`data`: DataFrame

    
    Returns:
        -`df_points`: DataFrame
    """
    # Adjust for team events by dropping duplicates based on team identifier
    data_with_unique = data_with.drop_duplicates(subset=["Event", "Team", "Year", "Medal"])
    data_without_unique = data_without.drop_duplicates(subset=["Event", "Team", "Year", "Medal"])

    df_points_with = data_with_unique.groupby(['NOC','Year'])[['Points', "Medals"]].sum().reset_index()
    df_points_with.columns = ['Country','Year','Points with', "Medals with"]

    df_points_without = data_without_unique.groupby(['NOC','Year'])[['Points', "Medals"]].sum().reset_index()
    df_points_without.columns = ['Country','Year','Points without', "Medals without"]
    
    df_merged = pd.merge(df_points_with, df_points_without, on=['Country','Year'], how='outer')

    return df_merged


def get_usefull_dataframe(df_final, pays, years):
    points_with = df_final[df_final["Country"] == pays]["Points with"].values
    points_without = df_final[df_final["Country"] == pays]["Points without"].values
    df = pd.DataFrame({
        "Year": years + years,
        "Type": ["With" for _ in years] + ["Without" for _ in years],
        "Points": list(points_with) + list(points_without)
    })
    return df



# Choix arbitraire + Mapping:
pays_dispo = [("USA", "United States"),
               ("CAN", "Canada"),
               ("FRA", "France"),
               ("GBR", "Great Britain"),
               ("GER", "Germany"),
               ("ITA", "Italy"),
               ("JPN", "Japan"),
               ("NED", "Netherlands"),
               ("NZL", "New-Zeland"),
               ("CHN", "China"),
               ("IND", "India"),
               ("AUS", "Australia"),
               ("BRA", "Brazil"),
               ("ESP", "Spain"),
               ("NOR", "Norway"),
               ("SWE", "Sweden"),
               ("FIN", "Finland")
               ]

pays_dispo = sorted(pays_dispo, key=lambda x: x[1])

def is_value_in_tuples(value, tuples_list):
    for tpl in tuples_list:
        if value in tpl:
            return tpl
    return None