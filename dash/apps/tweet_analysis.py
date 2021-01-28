import datetime
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output,State
import dash_daq as daq #pip install dash-daq
import pathlib

from app import app
from app import server

PATH=pathlib.Path(__file__).parent
DATA_PATH=PATH.joinpath("../datasets").resolve()
df=pd.read_csv(DATA_PATH.joinpath("tweets.csv"))

number_of_tweets=df['name'].count()
favourites_count=round(df['favourites_count'].sum()/1000000,2)
unique_users_count=df['name'].nunique()
sentiment_polarity=round(df['sentiment_polarity'].mean(),2)

# card definition
number_of_tweets_card = [
    # dbc.CardHeader("Countries",style={'text-align': 'center'}),
    dbc.CardBody(
        [
            html.H1(number_of_tweets, className="card-title"),
            html.P("Tweets Count",
                className="card-text",
            ),
        ],
        style={'text-align': 'center'}
    ),
]

favourites_count_card = [
    # dbc.CardHeader("Population",style={'text-align': 'center'}),
    dbc.CardBody(
        [
            html.H1(favourites_count, className="card-title"),
            html.P(
                "Tweets Likes (Mn)",
                className="card-text",
            ),
        ],
        style={'text-align': 'center'}
    ),
]

unique_users_count_card = [
    # dbc.CardHeader("GDP Per Capita",style={'text-align': 'center'}),
    dbc.CardBody(
        [
            html.H1(unique_users_count, className="card-title"),
            html.P(
                "Unique Users Tweeted",
                className="card-text",
            ),
        ],
        style={'text-align': 'center'}
    ),
]

sentiment_polarity_card = [
    # dbc.CardHeader("Expectancy",style={'text-align': 'center'}),
    dbc.CardBody(
        [
            html.H1(sentiment_polarity, className="card-title"),
            html.P(
                "Avg. Sentiment Polarity",
                className="card-text",
            ),
        ],
        style={'text-align': 'center'}
    ),
]
#end card definition


#layout
layout=dbc.Container([

	# navigation
	dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("World GDP Analysis", active=True,href="/apps/world_gdp_analysis")),
        dbc.NavItem(dbc.NavLink("Stock Market Analysis", active=True,href="/apps/stock_forecasting")),
        dbc.NavItem(dbc.NavLink("Tweets Analysis", active=True,href="/apps/tweet_analysis")),
        dbc.NavItem(dbc.NavLink("Tweets Topic Modeling", active=False,href="#"))
    ], 
    brand="Tweet Analysis",
    brand_href="/apps/home",
    color="primary",
    dark=True,
    style={'margin-bottom': '5px'}
	),#end navigation

# prompts row
	dbc.Row([
		# start sidebar
		dbc.Col([

			dcc.Dropdown(id='my-dpdn', multi=False, value='AMZN',
			# options=[{'label':x,'value':x} for x in sorted(df['Symbols'].unique())],
			style={'margin-bottom': '15px'}),

			dbc.Select(
			id="forecasting-frequency",value='6', options=[
	        {"label": "1", "value": "1"},
	        {"label": "2", "value": "2"},
	        {"label": "3",  "value": "3"},
	        {"label": "4", "value": "4"},
	        {"label": "5", "value": "5"},
	        {"label": "6",  "value": "6"},
	        {"label": "7", "value": "7"},
	        {"label": "8", "value": "8"},
	        {"label": "9",  "value": "9"},
	        {"label": "10", "value": "10"},
	        
	        ],style={'margin-bottom': '5px'}	          
	          ),

			dcc.Dropdown(id='my-dpdn2',multi=True, 
				# value=df['Symbols'].unique(),
			# options=[{'label':x,'value':x} for x in sorted(df['Symbols'].unique())],
			style={'margin-bottom': '10px'}),

			dcc.Dropdown(id='year-dropdown', multi=True, 
				# value=df['year_month'].unique(),
			# options=[{'label':x,'value':x} for x in sorted(df['year_month'].unique())],
			style={'margin-bottom': '10px'}),

			dcc.RadioItems(id='xlog_multi_type', 
                # options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'},
                style={'margin-bottom': '2px'})
		],
		md=3,
		style={'margin-bottom': '2px','margin-top': '2px','margin-left': '0px','border-style': 'solid','border-color': 'green'}
		),
		# end sidebar
	dbc.Col([
		html.Div(dbc.Row([
			html.Div(dbc.Card(number_of_tweets_card, color="primary", inverse=True)),
			html.Div(dbc.Card(favourites_count_card, color="primary", inverse=True),style={'padding-left': '50px'}),
			html.Div(dbc.Card(unique_users_count_card, color="primary", inverse=True),style={'padding-left': '50px'}),
			html.Div(dbc.Card(sentiment_polarity_card, color="primary", inverse=True),style={'padding-left': '50px'})]),
			style={'padding-left': '20px'}
			),
		html.Hr(),

		html.Div([
			daq.Gauge( id='sentiment-polarity-gauge', label="Sentiment", 
				color={"gradient":True,"ranges":{"red":[-1.00,0.03],"blue":[0.03,0.50],"green":[0.50,1.00]}},
				showCurrentValue=True,
				max=1,min=-1,
				value=sentiment_polarity),
			dcc.Graph(id='sentiment-polarity-graph', figure={})
			]
			)
			], 
			 md=9)
	], no_gutters=True,
	style={'margin-bottom': '1px'}),

# row 2 start
	dbc.Row([
		dbc.Col([
			dcc.Graph(id='line-fig2',figure={})
			]),
		dbc.Col([
			dcc.Graph(id='stackedbar-fig',figure={})
			]),
		], no_gutters=True,
		style={'height': '400px','margin-bottom': '2px'}),
	#row 2 end

	# row 3 start
	dbc.Row([
		dbc.Col([
			# dcc.Graph(id='forecasting_table',figure={})
			], md=0),
		dbc.Col([
			dcc.Graph(id='forecasting_graph_table',figure={})
			], md=12),
		dbc.Col([
			# dcc.Graph(id='forecasting_graph',figure={})
			], md=0),
		], no_gutters=True,
		style={'margin-bottom': '2px'}
		),
	#row 3 end

# row 1 start
dbc.Row([
	dbc.Col([
		# dcc.Graph(id='table-fig', figure={})
	
		]),
	], no_gutters=True),
# row 1 end

	  # footer
 		dbc.Row(
            [
                dbc.Col(html.Div("@galaxydataanalytics "),
                	style={
            'margin-top': '2px',
            'text-align':'center',
            'backgroundColor': 'rgba(120,120,120,0.2)'
            },
                 md=12)
            ]
        ),
        #end footer


	],
	fluid=True
	)


# @app.callback(
# Output('sentiment-polarity-gauge' , 'value')
# )
# def update_sentiment_polarity_gauge_graph(value):
# 	return value
	
			    # color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
			 #    value=2,
			 #    label='Default',
			 #    max=10,
			 #    min=0,
				# )  
	

# @app.callback(
# Output('line-fig2' , 'figure'),
# Input('my-dpdn2', 'value'),
# Input('xlog_multi_type', 'value'),
# Input('year-dropdown', 'value'),
# prevent_initial_call=False)
# def update_multi_graph(multi_stock_slctd,xlog_multi_type,date_selected):
# 	dff=df[df['Symbols'].isin(multi_stock_slctd) & df['year_month'].isin(date_selected)]	
# 	figln=px.line(dff,x='Date', y='High',color='Symbols',height=400)
# 	figln.update_yaxes(type='linear' if xlog_multi_type == 'Linear' else 'log')
# 	figln.update_xaxes(rangeslider_visible=False,
#     rangeselector=dict(
#         buttons=list([
#             dict(count=1, label="1m", step="month", stepmode="backward"),
#             dict(count=6, label="6m", step="month", stepmode="backward"),
#             dict(count=1, label="YTD", step="year", stepmode="todate"),
#             dict(count=1, label="1y", step="year", stepmode="backward"),
#             dict(step="all")
#         			])
#     				)
# 				)
# 	figln.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=0,b=0,l=0,r=0))
# 	return figln

# @app.callback(
# Output('stackedbar-fig' , 'figure'),
# Input('my-dpdn2', 'value'),
# Input('year-dropdown', 'value'),
# Input('xlog_multi_type', 'value'),
# prevent_initial_call=False)
# def update_stackedbar_graph(multi_stock_slctd,date_selected,xlog_multi_type):
# 	stock_stacked_df=pd.DataFrame(df.groupby(['year_month','Symbols'],as_index=False)['High'].mean()) #.sort_values(by=['gdpPercap'], ascending=True)
# 	dff=stock_stacked_df[stock_stacked_df['Symbols'].isin(multi_stock_slctd) & stock_stacked_df['year_month'].isin(date_selected)]	
# 	stacked_barchart=px.bar(dff,x='year_month',y='High',color='Symbols',text='High',height=400)
# 	stacked_barchart.update_yaxes(type='linear' if xlog_multi_type == 'Linear' else 'log')
# 	stacked_barchart.update_xaxes(rangeslider_visible=False,
#     rangeselector=dict(
#         buttons=list([
#             dict(count=1, label="1m", step="month", stepmode="backward"),
#             dict(count=6, label="6m", step="month", stepmode="backward"),
#             dict(count=1, label="YTD", step="year", stepmode="todate"),
#             dict(count=1, label="1y", step="year", stepmode="backward"),
#             dict(step="all")
#         			])
#     				)
# 				)
# 	stacked_barchart.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=0,b=0,l=0,r=0)) #use barmode='stack' when stacking,

# 	return stacked_barchart

