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

# from fbprophet import Prophet
import plotly.offline as py
import datetime
# import json
# from fbprophet.serialize import model_to_json, model_from_json


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
	        {"label": "11", "value": "11"},
	        {"label": "12", "value": "12"},
	        {"label": "13",  "value": "13"},
	        {"label": "14", "value": "14"},
	        {"label": "15", "value": "15"},
	        {"label": "16",  "value": "16"},
	        {"label": "17", "value": "17"},
	        {"label": "18", "value": "18"},
	        {"label": "19",  "value": "19"},
	        {"label": "20", "value": "20"},
	        {"label": "21", "value": "21"},
	        {"label": "22", "value": "22"},
	        {"label": "23",  "value": "23"},
	        {"label": "24", "value": "24"}
	        ],style={'margin-bottom': '5px'}	          
	          ),

			dcc.Dropdown(id='my-dpdn2',multi=True, value=df['Symbols'].unique(),
			options=[{'label':x,'value':x} for x in sorted(df['Symbols'].unique())],
			style={'margin-bottom': '10px'}),

			dcc.Dropdown(id='year-dropdown', multi=True, 
				value=df['year_month'].unique(),
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
	style={'height': '400px','margin-bottom': '1px'}),

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
	fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=0,b=0,l=0,r=0),height=400,
		title={'text': stock_slctd,'y':0.75,'x':0.4,'xanchor': 'center','yanchor': 'middle'})
	
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

# @app.callback(
# Output('table-fig' , 'figure'),
# Input('my-dpdn2', 'value'),
# Input('year-dropdown', 'value'),
# prevent_initial_call=False)
# def update_table_graph(multi_stock_slctd,date_selected):
# 	dff=df[df['Symbols'].isin(multi_stock_slctd) & df['year_month'].isin(date_selected)]	
# 	table_graph = go.Figure(data=[go.Table(header=dict(values=list(dff[['Date','Symbols','High','Low']].columns),fill_color='paleturquoise',
#                 align='left'),cells=dict(values=[dff.Date, dff.Symbols, dff.High, dff.Low],
#                fill_color='lavender',align='left'))])
# 	table_graph.update_layout(showlegend=False,autosize=True,margin=dict(t=0,b=0,l=0,r=0),height=350)
# 	return table_graph

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
# Output('forecasting_graph_table' , 'figure'),
# Input('my-dpdn', 'value'),
# Input('forecasting-frequency', 'value')
# )
# def update_forecasting_graph(stock_slctd,forecasting_frequency):
# 	df_fbp=df
# 	df_fbp['Date'] = pd.to_datetime(df_fbp['Date'], format='%Y-%m-%d')
# 	df_fbp['High'] = pd.to_numeric(df_fbp['High'],errors='ignore')
# 	df_fbp=df_fbp[df_fbp['Symbols'].isin([stock_slctd])]
# 	df_fbp=df_fbp[['Date','High']]
# 	df_fbp = df_fbp.rename(columns={'Date': 'ds', 'High': 'y'})
# 	df_fbp = df_fbp[df_fbp['ds']>='2020-01-02']
# 	estimated_months=int(forecasting_frequency)
# 	df_fbp = df_fbp[:-estimated_months]

# 	#1. Uncomment the below two lines when using trained model
# 	# with open('/app/apps/serialized_model.json', 'r') as fin:
# 	# 	model = model_from_json(json.load(fin))  # Load model after you've trained it  
# 	#2. Train your model in real-time
# 	model = Prophet(changepoint_prior_scale=0.5,yearly_seasonality=True,daily_seasonality=True)
# 	model.fit(df_fbp)
# 	df_forecast_2 = model.make_future_dataframe(periods= estimated_months, freq='M')
# 	df_forecast_2 = model.predict(df_forecast_2)
	
# 	fig = make_subplots(rows=1, cols=2,shared_xaxes=True,vertical_spacing=0.03,specs=[[{"type": "scatter"},{"type": "table"}]],
#     column_width=[0.8, 0.4],horizontal_spacing=0)

# 	fig.add_trace(go.Scatter(x=df_fbp['ds'], y=df_fbp['y'], name='Actual',line = dict(color='firebrick')),row=1, col=1) #dash='dash' to add line style
# 	fig.add_trace(go.Scatter(x=df_forecast_2['ds'], y=df_forecast_2['yhat'], name='Trend',line = dict(color='orange')),row=1, col=1)
# 	fig.add_trace(go.Scatter(x=df_forecast_2['ds'], y=df_forecast_2['yhat_upper'], name='Upper Band',line = dict(color='green'), fill = 'tonexty'),row=1, col=1)
# 	fig.add_trace(go.Scatter(x=df_forecast_2['ds'], y=df_forecast_2['yhat_lower'], name='Lower Band',line = dict(color='royalblue'),fill = 'tonexty'),row=1, col=1)
# 	fig.add_trace( go.Table(header=dict(values=df_forecast_2[['ds','trend','yhat_lower','yhat_upper','yhat']].columns,
# 	            font=dict(size=10),align="left"),cells=dict(values=[df_forecast_2.ds, round(df_forecast_2.trend,2), round(df_forecast_2.yhat_lower,2), round(df_forecast_2.yhat_upper,2),round(df_forecast_2.yhat,2)],
# 	            align = "left")),row=1, col=2)
# 	fig.update_layout(dict(title=stock_slctd,xaxis=dict(title = 'Period', ticklen=2, zeroline=False)),autosize=True,margin=dict(t=0,b=0,l=0,r=0))
# 	fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),title={'text': stock_slctd,'y':0.75,'x':0.4,'xanchor': 'center','yanchor': 'middle'})
	
# 	return fig





####### Training model for individual visualization. This is an inefficient way. The best alternative is to train a single model and use subplot to render the visualization as above
# # forecasting graph
# @app.callback(
# Output('forecasting_graph' , 'figure'),
# Input('my-dpdn', 'value'),
# Input('year-dropdown', 'value')
# )
# def update_forecasting_graph(stock_slctd,date_selected):
# 	df_fbp=df
# 	df_fbp['Date'] = pd.to_datetime(df_fbp['Date'], format='%Y-%m-%d')
# 	df_fbp['High'] = pd.to_numeric(df_fbp['High'],errors='ignore')
# 	df_fbp=df_fbp[df_fbp['Symbols'].isin([stock_slctd])]
# 	df_fbp=df_fbp[['Date','High']]
# 	df_fbp = df_fbp.rename(columns={'Date': 'ds', 'High': 'y'})
# 	df_fbp = df_fbp[df_fbp['ds']>='2020-01-02']
# 	estimated_months=6
# 	df_fbp = df_fbp[:-estimated_months]

# 	#1. Uncomment the below two lines when using trained model
# 	# with open('/app/apps/serialized_model.json', 'r') as fin:
# 	# 	model = model_from_json(json.load(fin))  # Load model after you've trained it  
# 	#2. Train your model in real-time
# 	model = Prophet(changepoint_prior_scale=0.5,yearly_seasonality=True,daily_seasonality=True)
# 	model.fit(df_fbp)

# 	df_forecast_2 = model.make_future_dataframe(periods= estimated_months, freq='M')
# 	df_forecast_2 = model.predict(df_forecast_2)
# 	# plot line graph
# 	fig=go.Figure()
# 	fig.add_trace(go.Scatter(x=df_fbp['ds'], y=df_fbp['y'], name='Actual',line = dict(color='firebrick'))) #dash='dash' to add line style
# 	fig.add_trace(go.Scatter(x=df_forecast_2['ds'], y=df_forecast_2['yhat'], name='Trend',line = dict(color='orange')))
# 	fig.add_trace(go.Scatter(x=df_forecast_2['ds'], y=df_forecast_2['yhat_upper'], name='Upper Band',line = dict(color='green'), fill = 'tonexty'))
# 	fig.add_trace(go.Scatter(x=df_forecast_2['ds'], y=df_forecast_2['yhat_lower'], name='Lower Band',line = dict(color='royalblue'),fill = 'tonexty'))
# 	fig.update_layout(dict(title=stock_slctd,xaxis=dict(title = 'Period', ticklen=2, zeroline=False)))
# 	# fig.add_annotation(align='center',valign='top',text=stock_slctd,showarrow=False,arrowhead=1)
	
# 	return fig



# # # forecasting table
# @app.callback(
# Output('forecasting_table' , 'figure'),
# Input('my-dpdn', 'value'),
# Input('year-dropdown', 'value')
# )
# def update_forecasting_table(stock_slctd,date_selected):
# 	df_fbp=df
# 	df_fbp['Date'] = pd.to_datetime(df_fbp['Date'], format='%Y-%m-%d')
# 	df_fbp['High'] = pd.to_numeric(df_fbp['High'],errors='ignore')
# 	df_fbp=df_fbp[df_fbp['Symbols'].isin([stock_slctd])]
# 	df_fbp=df_fbp[['Date','High']]
# 	df_fbp = df_fbp.rename(columns={'Date': 'ds', 'High': 'y'})
# 	df_fbp = df_fbp[df_fbp['ds']>='2020-01-02']
# 	estimated_months=6
# 	df_fbp = df_fbp[:-estimated_months]

# 	#1. Uncomment the below two lines when using trained model
# 	# with open('/app/apps/serialized_model.json', 'r') as fin:
# 	# 	model = model_from_json(json.load(fin))  # Load model after you've trained it  
# 	#2. Train your model in real-time
# 	model = Prophet(changepoint_prior_scale=0.5,yearly_seasonality=True,daily_seasonality=True)
# 	model.fit(df_fbp)

# 	df_forecast_2 = model.make_future_dataframe(periods= estimated_months, freq='M')
# 	df_forecast_2 = model.predict(df_forecast_2)
# 	# plot table
# 	table_forecasting = go.Figure(data=[go.Table(header=dict(values=list(df_forecast_2[['ds','trend','yhat_lower','yhat_upper','yhat']].columns),fill_color='paleturquoise',
#                 align='center'),cells=dict(values=[df_forecast_2.ds, df_forecast_2.trend, df_forecast_2.yhat_lower, df_forecast_2.yhat_upper,df_forecast_2.yhat],
#                fill_color='lavender',align='left'))])
# 	table_forecasting.update_layout(showlegend=False,autosize=True,margin=dict(t=0,b=0,l=0,r=0),height=350)
	
# 	return table_forecasting