import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output,State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from app import app, server
from apps import stock_forecasting

# Load and prepare data
# df2 = px.data.gapminder()
df = px.data.gapminder()
gdp_df=pd.DataFrame(df[df['year']==2007].groupby(['continent','year'],as_index=False)['gdpPercap'].mean())


# yearly_pop_df=pd.DataFrame(df2.groupby(['year'],as_index=False)['pop'].sum())
# df3=df2[['year', 'iso_alpha', 'lifeExp', 'gdpPercap']]
# 

# dash visualizations

def gdp_per_capita_by_continent(df):
    colors=['crimson','teal','skyblue','orange','green']
    yearly_gdp_df=pd.DataFrame(df.groupby(['year','continent'],as_index=False)['gdpPercap'].mean()).sort_values(by=['gdpPercap'], ascending=True)
    yearly_gdp_df=yearly_gdp_df.round(2)
    fig=px.bar(yearly_gdp_df,x='year',y='gdpPercap',color='continent',text='gdpPercap',height=350,color_discrete_sequence=colors,title='GDP Per Capita by Continent')
    fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=30,b=0,l=0,r=0)) #use barmode='stack' when stacking,
    return fig

def life_Exp_by_continent(df):
    lifeExp_df=pd.DataFrame(df[df['year']==2007].groupby(['continent'],as_index=False)['lifeExp'].mean()).sort_values(by=['lifeExp'], ascending=True)
    lifeExp_df=lifeExp_df.round(2)
    fig=px.bar(lifeExp_df,x='continent',y='lifeExp',text='lifeExp',color='lifeExp',height=350,title='Life Expectancy (2007)')
    fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=30,b=0,l=0,r=0))
    return fig
    
def population_distribution(df):
    df=pd.DataFrame(df[df['year']==2007].groupby(['continent'],as_index=False)['pop'].sum())
    df=df.round(2)
    colors=['crimson','teal','skyblue','orange','green']
    fig = go.Figure(data=[go.Pie(labels=df['continent'].tolist(), values=df['pop'].tolist(), hole=.3)])
    fig.update_layout(title={'text': 'Population Distribution','y':0.9,'x':0.5, 'xanchor': 'center','yanchor': 'top'},
        showlegend=False,autosize=True,annotations=[dict(text='Pop.',  font_size=20, showarrow=False)],margin=dict(t=50,b=0,l=0,r=0),
        height=350,colorway=colors)
    return fig

def population_growth(df):
    pop_df=pd.DataFrame(df[df['year']==2007].groupby(['continent'],as_index=False)['pop'].sum())
    pop_df=pop_df.round(2)
    pop_df=pop_df.sort_values(by=['pop'], ascending=True)
    colors=['teal']
    fig=px.bar(pop_df,y='continent',x='pop',text='pop',height=350,color_discrete_sequence=colors, title='Absolute Population (2007)')
    fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True,margin=dict(t=30,b=0,l=0,r=0))
    return fig

def population_trend(df):
    yearly_pop_df=pd.DataFrame(df.groupby(['year','continent'],as_index=False)['pop'].sum()).sort_values(by=['pop'], ascending=True)
    yearly_pop_df=yearly_pop_df.round(2)
    colors=['crimson','teal','skyblue','orange','green']
    fig = px.line(yearly_pop_df, x="year", y="pop",color='continent',height=350,color_discrete_sequence=colors,title='Population Growth Trend')
    fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01,orientation="h"),autosize=True,margin=dict(t=30,b=0,l=0,r=0))
    return fig

def gdp_lifeExp_distribution(df):
    yearly_avg_lifeExp_df=pd.DataFrame(df.groupby(['year'],as_index=False)['lifeExp'].mean())
    yearly_avg_gdp_df=pd.DataFrame(df.groupby(['year'],as_index=False)['gdpPercap'].mean())
    yearly_avg_lifeExp_df=yearly_avg_lifeExp_df.round(2)
    yearly_avg_gdp_df=yearly_avg_gdp_df.round(2)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=yearly_avg_lifeExp_df["year"], y=yearly_avg_lifeExp_df["lifeExp"], name="Life Expectancy"), secondary_y=False)
    fig.add_trace(go.Scatter(x=yearly_avg_gdp_df["year"], y=yearly_avg_gdp_df["gdpPercap"], name="GDP Per Capita"), secondary_y=True)
    fig.update_layout(title={'text': 'GDP Per Capita & Life Expectancy Trend','y':0.9,'x':0.5, 'xanchor': 'center','yanchor': 'top'},
        legend=dict(yanchor="top",y=0.85,xanchor="left",x=0.01,orientation="v"),autosize=True,margin=dict(t=30,b=0,l=0,r=0),height=350)
    return fig

def life_expectancy_geo(df):
    df=df[df['year']==2007]
    fig = px.choropleth(df, locations="iso_alpha",
                    color="lifeExp", 
                    hover_name="country", 
                    color_continuous_scale=px.colors.diverging.BrBG,
                    title="Life Expectancy Geo (2007)") 
    return fig

# cards
avg_gdp_per_capita=round(df[df['year']==2007]['gdpPercap'].mean(),2)
avg_life_exp=round(df[df['year']==2007]['lifeExp'].mean(),2)
total_population=round(df[df['year']==2007]['pop'].sum()/1000000000,2)
countries_analysed=df[df['year']==2007].groupby(['country'])['country'].nunique().sum()



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


layout=dbc.Container([
	# navigation
	dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("World GDP Analysis", active=True,href="/apps/world_gdp_analysis")),
        dbc.NavItem(dbc.NavLink("Stock Market Analysis", active=True,href="/apps/stock_forecasting")),
        dbc.NavItem(dbc.NavLink("Tweets Analysis", active=True,href="/apps/tweet_analysis")),
        dbc.NavItem(dbc.NavLink("Topic Modeling", active=True, href="/apps/topic_modeling"))
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

    # Performance Tiles
       dbc.Row(
            [
                dbc.Col(dbc.Card(card_content1, color="primary", inverse=True)),
                dbc.Col(dbc.Card(card_content2, color="secondary", inverse=True)),
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
		    id='gdp-per-capita-by-continent',
		    figure=gdp_per_capita_by_continent(df),
		    config={'displayModeBar': False }
		    )
                	),
                	md=4),
   #2.
            dbc.Col(html.Div(
            	dcc.Graph(
		    id='life-Exp-by-continent',
		    figure=life_Exp_by_continent(df),
		    config={'displayModeBar': False }
		    )
                	),
                	md=4),
   #3. population_growth
                dbc.Col(html.Div(
                dcc.Graph(
		    id='population_growth',
		    figure=population_distribution(df),
		    config={'displayModeBar': False }
		    )
                	),

                	md=4),

            ]
        ),

# 4. 
        dbc.Row(
            [
                dbc.Col(html.Div(

                dcc.Graph(
		    id='population-trend',
		    figure=population_trend(df),
		    config={'displayModeBar': False }
		    )
                	),

                	md=7),

    #5. 
           dbc.Col(html.Div(

                dcc.Graph(
		    id='population-growth',
		    figure=population_growth(df),
		    config={'displayModeBar': False }
		    )
                	),

                	md=5),
            ]
        ),
     #6. 

        dbc.Row(
            [
                dbc.Col(html.Div(
 			dcc.Graph(
		    id='gdp-lifeExp-distribution',
		    figure=gdp_lifeExp_distribution(df),
		    config={'displayModeBar': False }
		    )
                	),

                	md=5),

	#7.  
                dbc.Col(html.Div(
                   dcc.Graph(
		    id='life-expectancy-geo',
		    figure=life_expectancy_geo(df),
		    config={'displayModeBar': False }
		    )
                	),
                
                	md=7),
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


