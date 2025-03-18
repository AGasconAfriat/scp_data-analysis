from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"
)

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])
app.title = "SCP Status"

iris = px.data.iris()
gapminder = px.data.gapminder()
tips = px.data.tips()
carshare = px.data.carshare()

TEMPLATE = template_from_url(dbc.themes.DARKLY)

change_theme = ThemeChangerAIO(
    aio_id="theme",
    radio_props={"value": dbc.themes.DARKLY},
    button_props={
        "size": "lg",
        "outline": False,
        "style": {"marginTop": ".5rem"},
        "color": "success",
    },
)

# modes
modes = {0: "Default mode", 1: "Anti-memetic mode", 2: "Big egg"}

# Create list of dropdown menu items
season_select_list = []
for num, name in modes.items():
    season_select_list.append({"label": name, "value": num})

mode_select = dcc.Dropdown(options=season_select_list, value = 0, id='dashboard-mode')

@app.callback(
    Output("graphs", "children"),
    Input(component_id='dashboard-mode', component_property='value')
)
def make_figures(bleh): #input is currently ignored
    graph1 = dcc.Graph(
        figure=px.scatter(
            iris,
            x="sepal_width",
            y="sepal_length",
            color="species",
            title=f"Iris <br>{TEMPLATE} figure template",
            template=TEMPLATE,
        ),
        className="border",
    )
    graph2 = dcc.Graph(
        figure=px.scatter(
            gapminder,
            x="gdpPercap",
            y="lifeExp",
            size="pop",
            color="continent",
            hover_name="country",
            animation_frame="year",
            animation_group="country",
            log_x=True,
            size_max=60,
            title=f"Gapminder <br>{TEMPLATE} figure template",
            template=TEMPLATE,
        ),
        className="border",
    )
    graph3 = dcc.Graph(
        figure=px.violin(
            tips,
            y="tip",
            x="smoker",
            color="sex",
            box=True,
            points="all",
            hover_data=tips.columns,
            title=f"Tips <br>{TEMPLATE} figure template",
            template=TEMPLATE,
        ),
        className="border",
    )
    graph4 = dcc.Graph(
        figure=px.scatter_mapbox(
            carshare,
            lat="centroid_lat",
            lon="centroid_lon",
            color="peak_hour",
            size="car_hours",
            size_max=15,
            zoom=10,
            mapbox_style="carto-positron",
            title=f"Carshare <br> {TEMPLATE} figure template",
            template=TEMPLATE,
        ),
        className="border",
    )

    return [
        dbc.Row([dbc.Col(graph1, lg=6), dbc.Col(graph2, lg=6)]),
        dbc.Row([dbc.Col(graph3, lg=6), dbc.Col(graph4, lg=6)], className="mt-4"),
    ]


app.layout = dbc.Container(
    [
        dbc.Row(
            [
                #dbc.Col(change_theme, lg=2),
                dbc.Col(mode_select, lg=2)
            ],
        ),
        dbc.Row(dbc.Col(html.Div(id="graphs")))
    ],
    className="dbc p-4",
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True)