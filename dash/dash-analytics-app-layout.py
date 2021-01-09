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

df2 = px.data.gapminder()
gdp_df=pd.DataFrame(df2[df2['year']==2007].groupby(['continent','year'],as_index=False)['gdpPercap'].mean())
yearly_gdp_df=pd.DataFrame(df2.groupby(['year','continent'],as_index=False)['gdpPercap'].mean()).sort_values(by=['gdpPercap'], ascending=True)
lifeExp_df=pd.DataFrame(df2[df2['year']==2007].groupby(['continent'],as_index=False)['lifeExp'].mean()).sort_values(by=['lifeExp'], ascending=True)
yearly_lifeExp_df=pd.DataFrame(df2.groupby(['year','continent'],as_index=False)['lifeExp'].mean()).sort_values(by=['lifeExp'], ascending=True)
yearly_avg_lifeExp_df=pd.DataFrame(df2.groupby(['year'],as_index=False)['lifeExp'].mean())
yearly_pop_df=pd.DataFrame(df2.groupby(['year'],as_index=False)['pop'].sum())
pop_df=pd.DataFrame(df2[df2['year']==2007].groupby(['continent'],as_index=False)['pop'].mean())
# 

# dash visualizations
grouped_barchart=px.bar(yearly_gdp_df,x='year',y='gdpPercap',color='continent',text='gdpPercap')
grouped_barchart.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True) #use barmode='stack' when stacking,

barchart=px.bar(lifeExp_df,x='continent',y='lifeExp',text='lifeExp',color='lifeExp')
barchart.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True)

pop_barchart=px.bar(pop_df,y='continent',x='pop',text='pop',orientation='h')
pop_barchart.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True)

# donought pie chart with text at center
doughnut_pie_chart_with_center = go.Figure(data=[go.Pie(labels=df2['continent'].tolist(), values=df2['pop'].tolist(), hole=.3)])
doughnut_pie_chart_with_center.update_layout(showlegend=False,autosize=True,annotations=[dict(text='continent',  font_size=20, showarrow=False)])

# linegraph
life_exp_linegraph = px.line(yearly_lifeExp_df, x="year", y="lifeExp",color='continent')
life_exp_linegraph.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),autosize=True)

# line and bar
# line_bar_pop_gdp = px.line( x=yearly_lifeExp_df["year"].tolist(), y=yearly_lifeExp_df["lifeExp"].tolist())
# line_bar_pop_gdp.add_bar(pop_df,x=pop_df['year'].tolist(),y=pop_df['pop'].tolist(),text=pop_df['pop'].tolist(),color=pop_df['continent'].tolist())
# fig.add_bar(x=fruits, y=[2,1,3], name="Last year")

# line_bar_pop_gdp = px.line(x=yearly_avg_lifeExp_df["year"], y=yearly_avg_lifeExp_df["lifeExp"]) # labels=dict(x="Year", y="Pop", color="Time Period")
# line_bar_pop_gdp.add_bar(x=yearly_pop_df['year'], y=yearly_pop_df['pop'])

line_bar_pop_gdp = go.Figure()
line_bar_pop_gdp.add_trace(go.Scatter(x=yearly_avg_lifeExp_df["year"], y=yearly_avg_lifeExp_df["lifeExp"]))

# line_bar_pop_gdp.add_trace(
#     go.Bar(
#         x=[0, 1, 2, 3, 4, 5],
#         y=[1, 0.5, 0.7, -1.2, 0.3, 0.4]
#     ))



# cards
avg_gdp_per_capita=round(df2[df2['year']==2007]['gdpPercap'].mean(),2)
avg_life_exp=round(df2[df2['year']==2007]['lifeExp'].mean(),2)
total_population=round(df2[df2['year']==2007]['pop'].sum()/1000000000,2)
countries_analysed=df2[df2['year']==2007].groupby(['country'])['country'].nunique().sum()

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

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
                "Avg. GDP Per Capita Sold",
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
		    config={'displayModeBar': False }
		    # ,
		    # style={'width': '470px', 'height': '350px','margin-top': '0px','overflow': 'hidden'}
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
		    # ,
		    # style={'width': '470px', 'height': '350px','margin-top': '0px','overflow': 'hidden'}
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
		    # ,
		    # style={'width': '470px', 'height': '350px','margin-top': '0px','overflow': 'hidden'}
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
		    # ,
		    # style={'width': '470px', 'height': '350px','margin-top': '0px','overflow': 'hidden'}
		    )
                	),
			# style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                	md=9),

    #5. 
           dbc.Col(html.Div(

                dcc.Graph(
		    id='pop_barchart',
		    figure=pop_barchart,
		    config={'displayModeBar': False }
		    # ,
		    # style={'width': '470px', 'height': '350px','margin-top': '0px','overflow': 'hidden'}
		    )
                	),
			# style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                	md=3),
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
		    # ,
		    # style={'width': '470px', 'height': '350px','margin-top': '0px','overflow': 'hidden'}
		    )
                	),
			# style={
   #          'margin-top': '2px',
   #          'height': '300px',
   #          'backgroundColor': 'rgba(120,0,0,0.4)'
   #          },
                	md=9),

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