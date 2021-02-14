import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output,State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import pathlib

from app import app
from app import server


layout=dbc.Container([
	# navigation
	dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("World GDP Analysis", active=True,href="/apps/world_gdp_analysis")),
        dbc.NavItem(dbc.NavLink("Stock Market Analysis", active=True,href="/apps/stock_forecasting")),
        dbc.NavItem(dbc.NavLink("Tweets Analysis", active=True,href="/apps/tweet_analysis")),
        dbc.NavItem(dbc.NavLink("Topic Modeling", active=True, href="http://localhost:8866/#topic=2&lambda=1&term="))
        # html.Div(<a href="http://localhost:8866/#topic=2&lambda=1&term=">Topic Modeling</a>)
    ], 
    brand="Galaxy Analytics Dashbords",
    brand_href="/apps/home",
    color="primary",
    dark=True,
    style={'margin-bottom': '2px'}

),#end navigation

	#body
	 html.Div(
    [

  

    
    #1.
        dbc.Row(
            [
                dbc.Col(html.Div([
                  html.H6("World Gdp and Life Expectancy Analysis"),
                  html.Img(src=app.get_asset_url('world-gdp-analysis.png'), style={'height':'100%', 'width':'100%'})  
                  ] 
                	),
			style={
            'margin-top': '30px'
            },
                	md=4),
   #2.
                      dbc.Col(html.Div([
                    html.H6("Stock Market Forecasting") , 
                    html.Img(src=app.get_asset_url('stock-market-analysis.png'), style={'height':'100%', 'width':'100%'}) 
                    ]
                  ),
      style={
            'margin-top': '30px'
            },
                  md=4),
   #3. doughnut_pie_chart_with_center
                       dbc.Col(html.Div(
              [
                html.H6("Tweet Analysis") , 
                    html.Img(src=app.get_asset_url('tweet-analysis.png'), style={'height':'100%', 'width':'100%'}) 
              ]
                  ),
      style={
            'margin-top': '30px'
            },
                  md=4),

            ]
        ),

# 4. 
        dbc.Row(
            [
                        dbc.Col(html.Div(
     
                  ),
                  md=4),

    #5. 
                   dbc.Col(html.Div(
     
                  ),
                  md=4),

    # 6
                         dbc.Col(html.Div( 

                  ),
                  md=4),
            ]
        ),
     

       
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
        style={
            'padding-left': '3px',
            'padding-right': '3px'
            },
)
	#end body

	],
	fluid=True
	)


