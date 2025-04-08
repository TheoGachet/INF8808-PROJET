import dash
from dash import html
from visualisation_1.app import get_viz_1_html
from visualisation_2.src.app import get_viz_2_html
from visualisation_3.app import get_viz_3_html
from visualisation_4.app import get_viz_4_html
from visualisation_5.app import get_viz_5_html

app = dash.Dash(__name__)
app.title = "Projet INF8808"

app.layout = html.Div([
    html.Main([
        html.Div([
            html.Div([
                html.H1(
                    "What Makes a Nation Shine at the Olympics?",
                    className="section-title"
                ),
                html.P([
                    html.Br(),
                    "Every four years, the world turns its eyes to the Olympic Games.",
                    html.Br(),
                    "But behind the medals and the flags lies a deeper question:",
                    html.Br(),
                    html.Span("What really drives a country’s success on the world’s biggest stage?", style={"fontWeight": "bold"}),
                    html.Br(), html.Br(),
                    "Through this data-driven story, we explore three key dynamics that have shaped Olympic performance over the decades.",
                ], className="section-title"),
                html.Div([
                    html.A(
                        "Conditions du pays",
                        href="#viz2-section",
                        id="btn1"
                    ),
                    html.A(
                        "Spécialisation par sport",
                        href="#viz1-section",
                        id="btn2"
                    ),
                    html.A(
                        "Avantage à domicile",
                        href="#viz3-section",
                        id="btn3"
                    ),
                    html.A(
                        "Héros nationaux",
                        href="#viz4-section",
                        id="btn4"
                    ),
                    html.A(
                        "Impact individuel",
                        href="#viz5-section",
                        id="btn5"
                    ),
                ], className="ring-grid", style={'margin': '50px auto', 'width': 'fit-content'})
                ],
                className="section-column start p-40"    
            ),
            html.Div([
                    html.Img(src="assets/images/home_image.png", className="home-image")
                ],
                className="section-column center"    
            ),
            ], 
            className="section-row"
        ),
        html.Div(
            [get_viz_2_html()],
            id="viz2-section"
        ),
        html.Div(
            [get_viz_1_html()],
            id="viz1-section"
        ),
        html.Div(
            [get_viz_3_html()],
            id="viz3-section"
        ),
        html.Div(
            [get_viz_4_html()],
            id="viz4-section"
        ),
        html.Div(
            [get_viz_5_html()],
            id="viz5-section"
        ),
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
