import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output,State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from app import app
from app import server
from apps import stock_forecasting



layout=dbc.Container([
	# navigation
	dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("World GDP Analysis", active=True,href="/apps/world_gdp_analysis")),
        dbc.NavItem(dbc.NavLink("Stock Market Analysis", active=True,href="/apps/stock_forecasting")),
        dbc.NavItem(dbc.NavLink("Tweets Analysis", active=False,href="#")),
        dbc.NavItem(dbc.NavLink("Tweets Topic Modeling", active=False,href="#"))
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

  

    # Graphs
    #1.
        dbc.Row(
            [
                dbc.Col(html.Div(
     
                	),
			# style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                	md=4),
   #2.
                      dbc.Col(html.Div(
     
                  ),
      # style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                  md=4),
   #3. doughnut_pie_chart_with_center
                       dbc.Col(html.Div(
     
                  ),
      # style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                  md=4),

            ]
        ),

# 4. 
        dbc.Row(
            [
                        dbc.Col(html.Div(
     
                  ),
      # style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                  md=4),

    #5. 
                   dbc.Col(html.Div(
     
                  ),
      # style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                  md=4),
                          dbc.Col(html.Div(
     
                  ),
      # style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                  md=4),
            ]
        ),
     #6. 

       
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


