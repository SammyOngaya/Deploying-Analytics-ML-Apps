import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

# Load and prepare data
df2 = px.data.gapminder()
gdp_df=pd.DataFrame(df2[df2['year']==2007].groupby(['continent','year'],as_index=False)['gdpPercap'].mean())
yearly_gdp_df=pd.DataFrame(df2.groupby(['year','continent'],as_index=False)['gdpPercap'].mean()).sort_values(by=['gdpPercap'], ascending=True)
lifeExp_df=pd.DataFrame(df2[df2['year']==2007].groupby(['continent'],as_index=False)['lifeExp'].mean()).sort_values(by=['lifeExp'], ascending=True)
yearly_lifeExp_df=pd.DataFrame(df2.groupby(['year','continent'],as_index=False)['lifeExp'].mean()).sort_values(by=['lifeExp'], ascending=True)
yearly_avg_lifeExp_df=pd.DataFrame(df2.groupby(['year'],as_index=False)['lifeExp'].mean())
yearly_pop_df=pd.DataFrame(df2.groupby(['year'],as_index=False)['pop'].sum())
pop_df=pd.DataFrame(df2[df2['year']==2007].groupby(['continent'],as_index=False)['pop'].mean())
df3=df2[['year', 'iso_alpha', 'lifeExp', 'gdpPercap']]
# 

# dash visualizations
grouped_barchart=px.bar(yearly_gdp_df,x='year',y='gdpPercap',color='continent',text='gdpPercap',height=350)
grouped_barchart.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=0,b=0,l=0,r=0)) #use barmode='stack' when stacking,

barchart=px.bar(lifeExp_df,x='continent',y='lifeExp',text='lifeExp',color='lifeExp',height=350)
barchart.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=0,b=0,l=0,r=0))

pop_barchart=px.bar(pop_df,y='continent',x='pop',text='pop',height=350)
pop_barchart.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=0,b=0,l=0,r=0))

# donought pie chart with text at center
doughnut_pie_chart_with_center = go.Figure(data=[go.Pie(labels=df2['continent'].tolist(), values=df2['pop'].tolist(), hole=.3)])
doughnut_pie_chart_with_center.update_layout(showlegend=False,autosize=True,annotations=[dict(text='continent',  font_size=20, showarrow=False)],margin=dict(t=0,b=0,l=0,r=0),height=350)

# linegraph
life_exp_linegraph = px.line(yearly_lifeExp_df, x="year", y="lifeExp",color='continent',height=350)
life_exp_linegraph.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01,orientation="h"),autosize=True,margin=dict(t=0,b=0,l=0,r=0))

# line and bar
# Create figure with secondary y-axis
line_bar_pop_gdp = make_subplots(specs=[[{"secondary_y": True}]])
line_bar_pop_gdp.add_trace(go.Scatter(x=yearly_avg_lifeExp_df["year"], y=yearly_avg_lifeExp_df["lifeExp"], name="life expectancy"), secondary_y=False)
line_bar_pop_gdp.add_trace(go.Scatter(x=yearly_pop_df["year"], y=yearly_pop_df["pop"], name="population"), secondary_y=True)
line_bar_pop_gdp.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01,orientation="h"),autosize=True,margin=dict(t=0,b=0,l=0,r=0),height=350)

# cards
avg_gdp_per_capita=round(df2[df2['year']==2007]['gdpPercap'].mean(),2)
avg_life_exp=round(df2[df2['year']==2007]['lifeExp'].mean(),2)
total_population=round(df2[df2['year']==2007]['pop'].sum()/1000000000,2)
countries_analysed=df2[df2['year']==2007].groupby(['country'])['country'].nunique().sum()

#boxplot
gdp_boxplot = px.box(df2, x="year",y="lifeExp",height=350)
gdp_boxplot.update_layout(showlegend=False,autosize=True,margin=dict(t=0,b=0,l=0,r=0))

# table
table_graph = go.Figure(data=[go.Table(header=dict(values=list(df3.columns),fill_color='paleturquoise',
                align='left'),cells=dict(values=[df3.year, df3.iso_alpha, df3.lifeExp, df3.gdpPercap],
               fill_color='lavender',align='left'))])
table_graph.update_layout(showlegend=False,autosize=True,margin=dict(t=0,b=0,l=0,r=0),height=350)


# card definition
card_content1 = [
    dbc.CardHeader("Countries",style={'text-align': 'center'}),
    dbc.CardBody(
        [
            html.H1(countries_analysed, className="card-title"),
            html.P(
                "Countries Analysed",
                className="card-text",
            ),
        ],
        style={'text-align': 'center'}
    ),
]

card_content2 = [
    dbc.CardHeader("Population",style={'text-align': 'center'}),
    dbc.CardBody(
        [
            html.H1(total_population, className="card-title"),
            html.P(
                "Tota Population (Bn)",
                className="card-text",
            ),
        ],
        style={'text-align': 'center'}
    ),
]

card_content3 = [
    dbc.CardHeader("GDP Per Capita",style={'text-align': 'center'}),
    dbc.CardBody(
        [
            html.H1(avg_gdp_per_capita, className="card-title"),
            html.P(
                "Avg. GDP Per Capita",
                className="card-text",
            ),
        ],
        style={'text-align': 'center'}
    ),
]

card_content4 = [
    dbc.CardHeader("Expectancy",style={'text-align': 'center'}),
    dbc.CardBody(
        [
            html.H1(avg_life_exp, className="card-title"),
            html.P(
                "Avg. Life Expectancy",
                className="card-text",
            ),
        ],
        style={'text-align': 'center'}
    ),
]
#end card definition


app.layout=dbc.Container([
	# navigation
	dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("World GDP Analysis", active=True,href="#")),
        dbc.NavItem(dbc.NavLink("Tweets Analysis", active=True,href="#")),
        dbc.NavItem(dbc.NavLink("Tweets Topic Modeling", active=True,href="#"))
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
		    config={'displayModeBar': False }
		    )
                	),
			# style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                	md=4),
   #2.
            dbc.Col(html.Div(
            	dcc.Graph(
		    id='barchart',
		    figure=barchart,
		    config={'displayModeBar': False }
		    )
                	),
			# style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                	md=4),
   #3. doughnut_pie_chart_with_center
                dbc.Col(html.Div(
                dcc.Graph(
		    id='doughnut_pie_chart_with_center',
		    figure=doughnut_pie_chart_with_center,
		    config={'displayModeBar': False }
		    )
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

                dcc.Graph(
		    id='life_exp_linegraph',
		    figure=life_exp_linegraph,
		    config={'displayModeBar': False }
		    )
                	),
			# style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                	md=7),

    #5. 
           dbc.Col(html.Div(

                dcc.Graph(
		    id='pop_barchart',
		    figure=pop_barchart,
		    config={'displayModeBar': False }
		    )
                	),
			# style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                	md=5),
                # dbc.Col(html.Div("One of three columns"), md=4),
            ]
        ),
     #6. 

        dbc.Row(
            [
                dbc.Col(html.Div(
 			dcc.Graph(
		    id='line_bar_pop_gdp',
		    figure=line_bar_pop_gdp,
		    config={'displayModeBar': False }
		    )
                	),
			# style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                	md=4),

	#7.  
                dbc.Col(html.Div(

             dcc.Graph(
		    id='gdp_boxplot',
		    figure=gdp_boxplot,
		    config={'displayModeBar': False }
		    )
                	),
			# style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                	md=4),
    #8.
                dbc.Col(html.Div(
                   dcc.Graph(
		    id='table_graph',
		    figure=table_graph,
		    config={'displayModeBar': False }
		    )
                	),
			# style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                	md=4),
            ]
        ),

        # footer
 		dbc.Row(
            [
                dbc.Col(html.Div("footer"),
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

if __name__ == "__main__":
    app.run_server()