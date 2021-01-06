import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout=dbc.Container([
	# navigation
	dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Tweeter Analysis", active=True,href="#")),
        dbc.NavItem(dbc.NavLink("Temperature Analysis", active=True,href="#")),
        dbc.NavItem(dbc.NavLink("Titanic Analysis", active=True,href="#")),
        dbc.NavItem(dbc.NavLink("Iris Analysis", active=True,href="#"))
    ],
    brand="Galaxy Analytics Dashbords",
    brand_href="#",
    color="primary",
    dark=True,

),#end navigation

	#body
	 html.Div(
    [

      dbc.Row(
            [
                dbc.Col(html.Div("One of four columns"), width=6, lg=3),
                dbc.Col(html.Div("One of four columns"), width=6, lg=3),
                dbc.Col(html.Div("One of four columns"), width=6, lg=3),
                dbc.Col(html.Div("One of four columns"), width=6, lg=3),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"), md=4),
                dbc.Col(html.Div("One of three columns"), md=4),
                dbc.Col(html.Div("One of three columns"), md=4),
            ]
        ),
    ]
)
	#end body

	],
	fluid=True
	)

if __name__ == "__main__":
    app.run_server()