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
        ],
        style={'height': '75px',}
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
        ],
        style={'height': '75px',}
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
        ],
        style={'height': '75px'}
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
        ],
        style={'height': '75px'}
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
            className="mb-3"

        ),

        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"
                	),
			style={
            'margin-top': '2px',
            'height': '215px',
            'backgroundColor': 'rgba(120,0,0,0.4)'
            },
                	md=4),
                dbc.Col(html.Div("One of three columns")
               ,
			style={
            'margin-top': '2px',
            'height': '215px',
            'backgroundColor': 'rgba(0,120,0,0.4)'
            },
             md=4),
                dbc.Col(html.Div("One of three columns")

                ,
			style={
            'margin-top': '2px',
            'height': '215px',
            'backgroundColor': 'rgba(0,0,98,0.4)'
            },
             md=4),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns")
                	    ,
			style={
            'margin-top': '2px',
            'height': '215px',
            'backgroundColor': 'rgba(120,120,0,110)'
            },
                 md=9),
                dbc.Col(html.Div("One of three columns")
                    ,
			style={
            'margin-top': '2px',
            'height': '215px',
            'backgroundColor': 'rgba(120,105,73,0.2)'
            }, md=3),
                # dbc.Col(html.Div("One of three columns"), md=4),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"),
                	style={
            'margin-top': '2px',
            'height': '215px',
            'backgroundColor': 'rgba(120,10,73,0.2)'
            },
                 md=4),
                dbc.Col(html.Div("One of three columns"),
                style={
            'margin-top': '2px',
            'height': '215px',
            'backgroundColor': 'rgba(120,60,90,0.2)'
            }, md=4),
                dbc.Col(html.Div("One of three columns"),
                style={
            'margin-top': '2px',
            'height': '215px',
            'backgroundColor': 'rgba(0.4,120,40,0.4)'
            }, md=4),
            ]
        ),

        # footer
 		dbc.Row(
            [
                dbc.Col(html.Div("footer"),
                	style={
            'margin-top': '2px',
            'backgroundColor': 'rgba(120,120,120,0.2)'
            },
                 md=12)
            ]
        ),
        #end footer
    ],
        style={
            'padding-left': '5px',
            'padding-right': '5px'
            },
)
	#end body

	],
	fluid=True
	)

if __name__ == "__main__":
    app.run_server()