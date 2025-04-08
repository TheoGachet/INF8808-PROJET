import dash
from dash import html, dcc, Input, Output, callback
import visualisation_3.preprocess_ete_hiver as preprocess_ete_hiver
import visualisation_3.lolipop as lolipop

# Initial load
df = preprocess_ete_hiver.load_csv("all_athlete_games.csv")
df_filtered = preprocess_ete_hiver.preprocess_data(df, season="Summer")  # par défaut été
fig = lolipop.create_lollipop_figure(df_filtered, season="Summer")  # <-- saison ajoutée

def get_viz_3_html():
    return html.Div([
        html.Div([
            html.H1("🏟️ 2. Do Host Nations Really Have an Advantage?", style={'textAlign': 'center', 'marginBottom': '20px', "fontFamily": "Playfair Display"}),
            html.P([
                "Does being the host country boost your performance — or is it just a myth?",
                html.Br(),                
                "We compare how countries perform at home versus abroad to reveal if hosting gives athletes a psychological or logistical edge. The results may surprise you.",
            ], style={"textAlign": "justify", "backgroundColor": "#fdfdfd", 'marginBottom': '40px', "fontFamily": "Inter"}, 
                className="viz-description"
                )
        ]),
        html.Div([
            html.H2("Home Advantage at the Olympics: Myth or Reality?", style={"textAlign": "center", "color": "#DF0024", 'marginBottom': '40px', "fontFamily": "Playfair Display"}),
            html.Div(
                html.P(["It’s a question that sparks debate every few years — and now, the data speaks. This interactive visualization takes you on a journey through 75 years of Olympic history, comparing the performance of host nations at home versus abroad. For each country that has hosted the Games since 1945, we show how they’ve fared across three key indicators:",
                html.Br(), html.Br(),
                "• The average number of athletes they sent to compete",
                html.Br(),
                "• The average number of medals they won",
                html.Br(),
                "• And the efficiency of their teams, measured by medals per athlete",
                html.Br(), html.Br(),
                "The charts are split into two eras — 1945–1991 and 1992–2020 — to help you explore how the impact of hosting may have evolved over time."\
                "Each country appears twice: once for its performance as host, and once for when it competed away. Green dots represent results away from home, red dots show results on home ground, and the lines between them tell the story — of gains, gaps, and sometimes surprising reversals.",
                html.Br(), html.Br(),
                "👉 Hover over the charts to explore individual countries and uncover the patterns behind the podium." ,
                ], style={"textAlign": "justify", "fontFamily": "Inter"}
                ),
                className="viz-description"
            ),
            html.Div([
                dcc.RadioItems(
                    id='season-filter',
                    options=[
                        {"label": "Summer Olympics", "value": "Summer"},
                        {"label": "Winter Olympics", "value": "Winter"}
                    ],
                    value="Summer",
                    labelStyle={'display': 'inline-block', 'margin': '0 10px',"fontFamily": "Inter"},
                    inputStyle={"margin-right": "5px"}
                )
            ], style={'textAlign': 'center', 'margin': '20px 20px'}),
            dcc.Graph(id='lollipop-graph', figure=fig)
        ])
    ])


@callback(
    Output('lollipop-graph', 'figure'),
    Input('season-filter', 'value')
)
def update_figure(selected_season):
    df_filtered = preprocess_ete_hiver.preprocess_data(df, season=selected_season)
    fig = lolipop.create_lollipop_figure(df_filtered, season=selected_season)  # <-- saison ajoutée ici aussi
    return fig