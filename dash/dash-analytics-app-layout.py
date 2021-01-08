import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# Load data
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

df_fruit = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2]
})
# 

# dash visualizations
grouped_barchart=px.bar(df,x='Fruit',y='Amount',color='City',barmode='group',text='Amount')
grouped_barchart.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True)

barchart=px.bar(df_fruit,x='Fruit',y='Amount',text='Amount',color='Amount')
barchart.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True, xaxis={'categoryorder':'category descending'})

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
        dbc.NavItem(dbc.NavLink("Tweets Analysis", active=True,href="#")),
        dbc.NavItem(dbc.NavLink("Tweets Topic Modeling", active=True,href="#")),
        dbc.NavItem(dbc.NavLink("Temperature Analysis", active=True,href="#")),
        dbc.NavItem(dbc.NavLink("Titanic Analysis", active=True,href="#"))
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

    # Performance Tiles
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

    # Graphs
    #1.
        dbc.Row(
            [
                dbc.Col(html.Div(
                	  dcc.Graph(
		    id='grouped-bar-graph',
		    figure=grouped_barchart,
		    config={'displayModeBar': False },
		    style={'width': '470px', 'height': '350px','margin-top': '0px','overflow': 'hidden'}
		    )
                	),
			style={
            'margin-top': '2px',
            'height': '300px',
            'backgroundColor': 'rgba(120,0,0,0.4)'
            },
                	md=4),
   #2.
            dbc.Col(html.Div(dcc.Graph(
		    id='barchart',
		    figure=barchart,
		    config={'displayModeBar': False },
		    style={'width': '470px', 'height': '350px','margin-top': '0px','overflow': 'hidden'}
		    )
                	),
			style={
            'margin-top': '2px',
            'height': '300px',
            'backgroundColor': 'rgba(120,0,0,0.4)'
            },
                	md=4),
   #3.
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