import pandas_datareader.data as web
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


# Data scraping
# https://pandas-datareader.readthedocs.io/en/latest/remote_data.html#remote-data-stooq
# start = datetime.datetime(2020,1,1)
# end=datetime.datetime(2020,12,3)
# df=web.DataReader(['AMZN','GOOGL','FB'], 'stooq',start=start,end=end)
# df=df.stack().reset_index()
# # df.unstack().reset_index()
# print(df.head())
# df.to_csv("stock.csv",index=False)


df=pd.read_csv("data/stock.csv")
df['year_month']=pd.to_datetime(df['Date']).dt.strftime('%Y-%m')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],
	   meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])
server=app.server


# SIDEBAR_STYLE = {
#     "position": "fixed",
#     "top": 0,
#     "left": 0,
#     "bottom": 0,
#     "width": "16rem",
#     "padding": "2rem 1rem",
#     "background-color": "#f8f9fa",
# }

#layout
app.layout=dbc.Container([

	# navigation
	dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("World GDP Analysis", active=False,href="#")),
        dbc.NavItem(dbc.NavLink("Stock Market Analysis", active=True,href="#")),
        dbc.NavItem(dbc.NavLink("Tweets Analysis", active=False,href="#")),
        dbc.NavItem(dbc.NavLink("Tweets Topic Modeling", active=False,href="#"))
    ], 
    brand="Stock Market Forecasting",
    brand_href="#",
    color="primary",
    dark=True,
    style={'margin-bottom': '2px'}
	),#end navigation

# prompts row
	dbc.Row([
		# start sidebar
		dbc.Col([

			dcc.Dropdown(id='my-dpdn', multi=False, value='AMZN',
			options=[{'label':x,'value':x} for x in sorted(df['Symbols'].unique())]),

			dcc.Dropdown(id='my-dpdn2',multi=True, value=df['Symbols'].unique(),
			options=[{'label':x,'value':x} for x in sorted(df['Symbols'].unique())]),

			dcc.Dropdown(id='year-dropdown', multi=True, value=df['year_month'].unique(),
			options=[{'label':x,'value':x} for x in sorted(df['year_month'].unique())]),

			dcc.RadioItems(id='xlog_multi_type', 
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'})
		],
		md=3
		),
		# end sidebar
	dbc.Col([
		dcc.Graph(id='line-fig', figure={})
		], md=9)
	], no_gutters=True),

# row 2 start
	dbc.Row([
		dbc.Col([
			dcc.Graph(id='line-fig2',figure={})
			]),
		dbc.Col([
			dcc.Graph(id='stackedbar-fig',figure={})
			]),
		], no_gutters=True),
	#row 2 end

# row 1 start
dbc.Row([
	dbc.Col([
		dcc.Graph(id='table-fig', figure={})
	
		]),
	], no_gutters=True),
# row 1 end


	],
	fluid=True
	)


# callbacks
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
	fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=0,b=0,l=0,r=0))
	
	return fig

@app.callback(
Output('line-fig2' , 'figure'),
Input('my-dpdn2', 'value'),
Input('xlog_multi_type', 'value'),
Input('year-dropdown', 'value'),
prevent_initial_call=False)
def update_multi_graph(multi_stock_slctd,xlog_multi_type,date_selected):
	dff=df[df['Symbols'].isin(multi_stock_slctd) & df['year_month'].isin(date_selected)]	
	figln=px.line(dff,x='Date', y='High',color='Symbols')
	figln.update_yaxes(type='linear' if xlog_multi_type == 'Linear' else 'log')
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
	stacked_barchart=px.bar(dff,x='year_month',y='High',color='Symbols',text='High',height=350)
	stacked_barchart.update_yaxes(type='linear' if xlog_multi_type == 'Linear' else 'log')
	stacked_barchart.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=0,b=0,l=0,r=0)) #use barmode='stack' when stacking,

	return stacked_barchart


if __name__ == "__main__":
    app.run_server()