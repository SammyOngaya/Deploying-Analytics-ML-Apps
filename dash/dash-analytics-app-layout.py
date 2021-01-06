import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# card definition
card_content1 = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]

card_content2 = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]

card_content3 = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]

card_content4 = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]
#end card definition


app.layout=dbc.Container([
	# navigation
	dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Tweeter Analysis", active=True,href="#")),
        dbc.NavItem(dbc.NavLink("Temperature Analysis", active=True,href="#")),
        dbc.NavItem(dbc.NavLink("Titanic Analysis", active=True,href="#")),
        dbc.NavItem(dbc.NavLink("Iris Analysis", active=True,href="#"))
    ],
    brand="Galaxy Analytics Dashbords",
    brand_href="#",
    color="primary",
    dark=True,
    style={'margin-bottom': '2px'}

),#end navigation

	#body
	 html.Div(
    [

       dbc.Row(
            [
                dbc.Col(dbc.Card(card_content1, color="primary", inverse=True)),
                dbc.Col(
                    dbc.Card(card_content2, color="secondary", inverse=True)
                ),
                dbc.Col(dbc.Card(card_content3, color="info", inverse=True)),
                dbc.Col(dbc.Card(card_content4, color="success", inverse=True)),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"), md=4),
                dbc.Col(html.Div("One of three columns"), md=4),
                dbc.Col(html.Div("One of three columns"), md=4),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"), md=9),
                dbc.Col(html.Div("One of three columns"), md=3),
                # dbc.Col(html.Div("One of three columns"), md=4),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"), md=4),
                dbc.Col(html.Div("One of three columns"), md=4),
                dbc.Col(html.Div("One of three columns"), md=4),
            ]
        ),
    ]
)
	#end body

	],
	fluid=True
	)

if __name__ == "__main__":
    app.run_server()