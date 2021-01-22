# import pandas_datareader.data as web
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
import pathlib

from fbprophet import Prophet
import plotly.offline as py
import datetime


from app import app


# Data scraping
# https://pandas-datareader.readthedocs.io/en/latest/remote_data.html#remote-data-stooq
# start = datetime.datetime(2020,1,1)
# end=datetime.datetime(2020,12,3)
# df=web.DataReader(['AMZN','GOOGL','FB'], 'stooq',start=start,end=end)
# df=df.stack().reset_index()
# # df.unstack().reset_index()
# print(df.head())
# df.to_csv("stock.csv",index=False)

PATH=pathlib.Path(__file__).parent
DATA_PATH=PATH.joinpath("../datasets").resolve()

df=pd.read_csv(DATA_PATH.joinpath("stock.csv"))
df['year_month']=pd.to_datetime(df['Date']).dt.strftime('%Y-%m')

# df_fbp=df.copy()
# df_fbp['Date'] = pd.to_datetime(df_fbp['Date'], format='%Y-%m-%d')
# df_fbp['High'] = pd.to_numeric(df_fbp['High'],errors='ignore')
# df_fbp=df_fbp[df_fbp['Symbols']=='AMZN']
# df_fbp=df_fbp[['Date','High']]
# df_fbp = df_fbp.rename(columns={'Date': 'ds', 'High': 'y'})
# df_fbp = df_fbp[df_fbp['ds']>='2020-01-02']
# df_fbp0=df_fbp.copy()
# estimated_days=6
# df_fbp = df_fbp[:-estimated_days]
# df_model = Prophet(changepoint_prior_scale=0.5,yearly_seasonality=True,daily_seasonality=True)
# df_model.fit(df_fbp)
# df_forecast = df_model.make_future_dataframe(periods= estimated_days, freq='M')
# df_forecast = df_model.predict(df_forecast)

#layout
layout=dbc.Container([

	# navigation
	dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("World GDP Analysis", active=True,href="/apps/world_gdp_analysis")),
        dbc.NavItem(dbc.NavLink("Stock Market Analysis", active=True,href="/apps/stock_forecasting")),
        dbc.NavItem(dbc.NavLink("Tweets Analysis", active=False,href="#")),
        dbc.NavItem(dbc.NavLink("Tweets Topic Modeling", active=False,href="#"))
    ], 
    brand="Stock Market Forecasting",
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
			options=[{'label':x,'value':x} for x in sorted(df['Symbols'].unique())],
			style={'margin-bottom': '15px'}),

			dcc.Dropdown(id='my-dpdn2',multi=True, value=df['Symbols'].unique(),
			options=[{'label':x,'value':x} for x in sorted(df['Symbols'].unique())],
			style={'margin-bottom': '10px'}),

			dcc.Dropdown(id='year-dropdown', multi=True, value=df['year_month'].unique(),
			options=[{'label':x,'value':x} for x in sorted(df['year_month'].unique())],
			style={'margin-bottom': '10px'}),

			dcc.RadioItems(id='xlog_multi_type', 
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'},
                style={'margin-bottom': '2px'})
		],
		md=3,
		style={'margin-bottom': '2px','margin-top': '2px','margin-left': '0px','border-style': 'solid','border-color': 'green'}
		),
		# end sidebar
	dbc.Col([
		dcc.Graph(id='line-fig', figure={})
		], md=9)
	], no_gutters=True,
	style={'height': '400px','margin-bottom': '5px'}),

# row 2 start
	dbc.Row([
		dbc.Col([
			dcc.Graph(id='line-fig2',figure={})
			]),
		dbc.Col([
			dcc.Graph(id='stackedbar-fig',figure={})
			]),
		], no_gutters=True,
		style={'height': '500px','margin-bottom': '2px'}),
	#row 2 end

	# row 3 start
	dbc.Row([
		dbc.Col([
			dcc.Graph(id='forecasting_table',figure={})
			]),
		dbc.Col([
			dcc.Graph(id='forecasting_graph',figure={})
			]),
		], no_gutters=True,
		style={'height': '500px','margin-bottom': '2px'}),
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


@app.callback(
Output('line-fig' , 'figure'),
Input('my-dpdn', 'value'),
Input('year-dropdown', 'value')
)
def update_graph(stock_slctd,date_selected):
	dff=df[df['Symbols'].isin([stock_slctd]) & df['year_month'].isin(date_selected)]
	fig=go.Figure()
	fig.add_trace(go.Scatter(x=dff['Date'], y=dff['High'], name='High',line = dict(color='green'))) #dash='dash' to add line style
	fig.add_trace(go.Scatter(x=dff['Date'], y=dff['Low'], name='Low',line = dict(color='firebrick')))
	fig.add_trace(go.Scatter(x=dff['Date'], y=dff['Open'], name='Open',line = dict(color='orange')))
	fig.add_trace(go.Scatter(x=dff['Date'], y=dff['Close'], name='Close',line = dict(color='royalblue')))
	fig.update_xaxes(rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        			])
    				)
				)
	fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=0,b=0,l=0,r=0),height=400)
	
	return fig

@app.callback(
Output('line-fig2' , 'figure'),
Input('my-dpdn2', 'value'),
Input('xlog_multi_type', 'value'),
Input('year-dropdown', 'value'),
prevent_initial_call=False)
def update_multi_graph(multi_stock_slctd,xlog_multi_type,date_selected):
	dff=df[df['Symbols'].isin(multi_stock_slctd) & df['year_month'].isin(date_selected)]	
	figln=px.line(dff,x='Date', y='High',color='Symbols',height=400)
	figln.update_yaxes(type='linear' if xlog_multi_type == 'Linear' else 'log')
	figln.update_xaxes(rangeslider_visible=False,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        			])
    				)
				)
	figln.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=0,b=0,l=0,r=0))
	return figln

@app.callback(
Output('table-fig' , 'figure'),
Input('my-dpdn2', 'value'),
Input('year-dropdown', 'value'),
prevent_initial_call=False)
def update_table_graph(multi_stock_slctd,date_selected):
	dff=df[df['Symbols'].isin(multi_stock_slctd) & df['year_month'].isin(date_selected)]	
	table_graph = go.Figure(data=[go.Table(header=dict(values=list(dff[['Date','Symbols','High','Low']].columns),fill_color='paleturquoise',
                align='left'),cells=dict(values=[dff.Date, dff.Symbols, dff.High, dff.Low],
               fill_color='lavender',align='left'))])
	table_graph.update_layout(showlegend=False,autosize=True,margin=dict(t=0,b=0,l=0,r=0),height=350)
	return table_graph

	# 
@app.callback(
Output('stackedbar-fig' , 'figure'),
Input('my-dpdn2', 'value'),
Input('year-dropdown', 'value'),
Input('xlog_multi_type', 'value'),
prevent_initial_call=False)
def update_stackedbar_graph(multi_stock_slctd,date_selected,xlog_multi_type):
	stock_stacked_df=pd.DataFrame(df.groupby(['year_month','Symbols'],as_index=False)['High'].mean()) #.sort_values(by=['gdpPercap'], ascending=True)
	dff=stock_stacked_df[stock_stacked_df['Symbols'].isin(multi_stock_slctd) & stock_stacked_df['year_month'].isin(date_selected)]	
	stacked_barchart=px.bar(dff,x='year_month',y='High',color='Symbols',text='High',height=400)
	stacked_barchart.update_yaxes(type='linear' if xlog_multi_type == 'Linear' else 'log')
	stacked_barchart.update_xaxes(rangeslider_visible=False,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        			])
    				)
				)
	stacked_barchart.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=0,b=0,l=0,r=0)) #use barmode='stack' when stacking,

	return stacked_barchart

# forecasting graph

# @app.callback(
# Output('forecasting_graph' , 'figure'),
# # Input('my-dpdn2', 'value')
# )
# def update_forecasting_graph():
# 	actual_stock = go.Scatter(
# 	    name = 'Actual Stock',
# 	   mode = 'lines',
# 	   x = list(df_fbp0['ds']),
# 	   y = list(df_fbp0['y']),
# 	   marker=dict(
# 	      color='black',
# 	      line=dict(width=2)
# 	   )
# 	)

# 	trend = go.Scatter(
# 	    name = 'trend',
# 	    mode = 'lines',
# 	    x = list(df_forecast['ds']),
# 	    y = list(df_forecast['yhat']),
# 	    marker=dict(
# 	        color='orange',
# 	        line=dict(width=3)
# 	    )
# 	)


# 	upper_band = go.Scatter(
# 	    name = 'upper band',
# 	    mode = 'lines',
# 	    x = list(df_forecast['ds']),
# 	    y = list(df_forecast['yhat_upper']),
# 	    line= dict(color='green'),
# 	    fill = 'tonexty'
# 	)

# 	lower_band = go.Scatter(
# 	    name= 'lower band',
# 	    mode = 'lines',
# 	    x = list(df_forecast['ds']),
# 	    y = list(df_forecast['yhat_lower']),
# 	    line= dict(color='blue')
# 	)


# 	plot_data = [trend, lower_band, upper_band,actual_stock]

# 	layout = dict(title='Stock Forecasting',
# 	             xaxis=dict(title = 'Dates', ticklen=2, zeroline=False))

# 	figure=dict(data=plot_data,layout=layout)
# 	figure=py.offline.iplot(figure)
# 	return figure
