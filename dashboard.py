from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import kagglehub
import pandas as pd
import matplotlib.pyplot as plt
import math
import re
import plotly.graph_objects as go
import plotly.express as px

def contains_count(string, elements):
    count = 0
    for element in elements:
        count += string.count(element)
    return count
def get_class(text):
    x = re.findall(r"\n (\w*) Class: (\w*) \n", text)
    if x :
        return(list(x[0]))
    else:
        return ["None", "None"]
def get_class_type(text):
    return get_class(text)[0]
def get_class_spec(text):
    return get_class(text)[1]
def get_series(scp_code):
    num = int(scp_code[4:])
    return math.ceil(num/1000)

pd.set_option('display.max_colwidth', None)

#TODO set back to download after development
#path = kagglehub.dataset_download("czzzzzzz/scp1to7")
#df = pd.read_csv(f"{path}/scp6999.csv")
df = pd.read_csv("scp6999.csv")

df["class type"] = df["text"].apply(get_class_type)
df["class"] = df["text"].apply(get_class_spec)
df["series"] = df["code"].apply(get_series)

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
def make_figures(current_mode):
    #graph1 = dcc.Graph(
    #    figure=px.scatter(
    #        iris,
    #        x="sepal_width",
    #        y="sepal_length",
    #        color="species",
    #        title=f"Iris <br>{TEMPLATE} figure template",
    #        template=TEMPLATE,
    #    ),
    #    className="border",
    #)
    # Graph 1 : Distribution of SCPs by containment class by series ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    primary_classes=["Safe", "Euclid", "Keter"]
    primary_classes_df = df[df["class"].isin(primary_classes)]
    class_counts = primary_classes_df.groupby(["class", "series"]).count().reset_index()
    x_data = class_counts["class"].tolist()
    y_data = class_counts["code"].tolist()
    color_data = class_counts["series"].tolist()
    data = {"class": x_data,
            "total SCPs": y_data,
            "series": color_data}
    hist_df = pd.DataFrame(data)
    fig1 = px.histogram(hist_df, x="class", y="total SCPs", color="series", color_discrete_sequence=px.colors.sequential.Plasma_r, barmode="group",
                      title="Distribution of SCPs by containment class by series")
    #fig1 = px.histogram(x=x_data, y=y_data, color=color_data, color_discrete_sequence=px.colors.sequential.Plasma_r, barmode="group",
    #                  title="Distribution of SCPs by containment class by series")
    fig1.update_layout(yaxis_title="")
    fig1.update_layout(xaxis_title="class")
    fig1.update_traces(hovertemplate='Total SCPs: %{y}<extra></extra>')

    
    graph1 = dcc.Graph(
        figure = fig1,
        className="border",
    )

    if current_mode !=2:
        title2 = f"Gapminder <br>{TEMPLATE} figure template"
    else:
        title2 = "Big egg"
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
            title=title2,
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