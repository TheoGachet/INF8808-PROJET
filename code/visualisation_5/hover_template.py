import preprocess

pays_disponibles = preprocess.pays_dispo

def get_hovertemplate(pays):
    _, full_pays = preprocess.is_value_in_tuples(pays, pays_disponibles)

    hovertemplate = (f"<extra></extra><br>" +
                     "Year: %{customdata[0]}<br>" + 
                     "Country: " + str(full_pays) + "<br>" +
                     "%{y} points <br>") 
    return hovertemplate