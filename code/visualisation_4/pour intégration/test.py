from init import get_output

if __name__ == "__main__":
    # Exemple de test pour la fonction get_output
    season = "Summer"      # ou "Winter"
    discipline = "Athletics"  # remplacez par une discipline présente dans disciplines_summer.csv
    output_components = get_output(season, discipline)
    for comp in output_components:
        print(comp)
