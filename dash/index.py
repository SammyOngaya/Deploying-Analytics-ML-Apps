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
from apps import stock_forecasting,world_gdp_analysis,home,tweet_analysis,topic_modeling


app.layout = html.Div([
  dcc.Location(id='url', refresh=False),
   html.Div(id='page-content'),
  
])


# links method
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/stock_forecasting':
        return stock_forecasting.layout
    elif pathname == '/apps/world_gdp_analysis':
        return world_gdp_analysis.layout
    elif pathname == '/apps/home':
        return home.layout
    elif pathname == '/apps/tweet_analysis':
        return tweet_analysis.layout
    elif pathname == '/apps/topic_modeling':
        return topic_modeling.layout
    else:
        return ''

if __name__ == '__main__':
    app.run_server(debug=False)