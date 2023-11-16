from dash import html
import dash_bootstrap_components as dbc


class Project:
    def __init__(self, name, description, link, thumbnail):
        self.name = name
        self.description = description
        self.link = link
        self.thumbnail = thumbnail

    def to_card(self):
        return dbc.Card(
            [
                dbc.CardImg(src=f"/assets/{self.thumbnail}", top=True),
                dbc.CardBody(
                    [
                        html.H4(f"{self.name}", className="card-title"),
                        html.P(f"{self.description}"),
                        dbc.Button(f"View Demo", href=f"{self.link}", color="primary")
                    ]
                ),
            ],
            style={"width": "25vw"},
            className="mb-4"
        )
