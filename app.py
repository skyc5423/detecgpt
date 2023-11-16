import dash
from dash import html
import dash_bootstrap_components as dbc
import yaml
from project import Project

with open('demo_list.yaml', 'r') as f:
    demo_list = yaml.safe_load(f)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H1("Welcome to My Playground!", className="display-3 text-white"),
                        html.P(
                            "This is my playground where I play with GPT, ML, CV, DL, AI, etc.!.",
                            className="lead text-white"
                        ),
                    ],
                    className="text-center py-5",
                ),
                width=12
            ),
            className="mb-4"
        ),
        dbc.Row(
            [
                dbc.Col(Project(**demo).to_card()) for demo in demo_list
            ],
            id="projects",
            style={"padding-left": "5vw", "padding-right": "5vw"},
        )
    ],
    fluid=True
)

if __name__ == '__main__':
    app.run_server(debug=True)
