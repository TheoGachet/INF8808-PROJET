import pandas as pd
import plotly.express as px
from preprocess import *
from dash import dcc, html, Dash
from dash.dependencies import Input, Output

pays = "USA"
usefull_df = get_usefull_dataframe_rank(pays)

# Création du slopechart
fig = px.line(usefull_df, x="Type", y="Points", color="Year",
              color_discrete_sequence=px.colors.sequential.Blues[1:],
              markers=True,
              title=str("Slopechart des points de " + pays + " avec et sans leurs athlètes multi-médaillés")
              )

# Personnalisation
fig.update_traces(line=dict(width=2),
                  hovertemplate=f"<extra></extra><br>" +
                  "%{y} Points")

fig.update_layout(xaxis=dict(type='category'),  # Forcer l'axe X en catégorie
                  width=700, height=700,  
                  xaxis_showgrid=False,  
                  yaxis_showgrid=False,
                  plot_bgcolor = 'lightgrey'), 


# Liste des pays disponibles
pays_disponibles = sigles_pays

# Création de l'application Dash
app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown-pays',
        options=[{'label': p, 'value': p} for p in pays_disponibles],
        value=pays,  # Valeur par défaut
        placeholder="Sélectionnez un pays"
    ),
    dcc.Graph(id='slopechart')
])

@app.callback(
    Output('slopechart', 'figure'),
    [Input('dropdown-pays', 'value')]
)
def update_slopechart(pays_selectionne):
    usefull_df = get_usefull_dataframe_rank(pays_selectionne)
    fig = px.line(usefull_df, x="Type", y="Points", color="Year",
                  color_discrete_sequence=px.colors.sequential.Blues[1:],
                  markers=True,
                  title=str("Slopechart des points de " + pays_selectionne + " avec et sans leurs athlètes multi-médaillés")
                  )
    fig.update_traces(line=dict(width=2),
                      hovertemplate=f"<extra></extra><br>" + "%{y} Points")
                    
    fig.update_layout(xaxis=dict(type='category'),
                      width=800, height=800,
                      xaxis_showgrid=False, yaxis_showgrid=False,
                      plot_bgcolor='lightgrey')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)