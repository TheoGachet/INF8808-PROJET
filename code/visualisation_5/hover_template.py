import visualisation_5.preprocess as preprocess

pays_disponibles = preprocess.pays_dispo

def get_hovertemplate(pays):
    _, full_pays = preprocess.is_value_in_tuples(pays, pays_disponibles)

    hovertemplate = (f"<extra></extra><br>" +
                     "<b style='font-family:Inter;'>Year:</b> %{customdata[0]}<br>" + 
                     "<b style='font-family:Inter;'>Country:</b> " + str(full_pays) + "<br>" +
                     "<b style='font-family:Inter;'>%{y} points</b> <br>") 
    return hovertemplate