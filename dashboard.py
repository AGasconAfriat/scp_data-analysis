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

pd.set_option('display.max_colwidth', None)

df = pd.read_csv("scp6999augmented.csv")

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

links = html.Div(
    [
        html.Label(
            [
                html.A(
                    "SCP Wiki",
                    href="https://scp-wiki.wikidot.com/",
                    target="_blank",
                ),
                " | ",
                html.A(
                    "Antimemetics Division",
                    href="https://scp-wiki.wikidot.com/antimemetics-division-hub",
                    target="_blank",
                ),
                " | ",
                html.A(
                    "SCP-Big egg",
                    href="https://scp-wiki.wikidot.com/scp-big-egg-j",
                    target="_blank",
                ),
            ]
        ),
    ]
)

@app.callback(
    Output("graphs", "children"),
    Input(component_id='dashboard-mode', component_property='value')
)
def make_figures(current_mode):
    #pd.options.mode.copy_on_write = True
    # Graph 1 : Distribution of SCPs by containment class by series ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    primary_classes=["Safe", "Euclid", "Keter"]
    primary_classes_df = df[df["class"].isin(primary_classes)]
    if current_mode != 2:
        title1 = "Distribution of SCPs by containment class by series"
        ytitle1 = ""
        hovertempl1 = "Total SCPs: %{y}<extra></extra>"
        xtitle1 = "class"
    else:
        title1 = "Bigness and roundness"
        ytitle1 = "bigness"
        hovertempl1 = "Total bigness: %{y} big<extra></extra>"
        xtitle1 = "roundness"
        is_safe = (primary_classes_df["class"] == "Safe")
        is_euclid = (primary_classes_df["class"] == "Euclid")
        is_keter = (primary_classes_df["class"] == "Keter")
        primary_classes_df.loc[is_safe, "class"] = "Big round"
        primary_classes_df.loc[is_euclid, "class"] = "Round"
        primary_classes_df.loc[is_keter, "class"] = "Kind of round"
        primary_classes=["Big round", "Round", "Kind of round"]
    class_counts = primary_classes_df.groupby(["class", "series"]).count().reset_index()
    fig1 = px.histogram(class_counts, x="class", y="code", color="series", color_discrete_sequence=px.colors.sequential.Plasma_r, barmode="group",
                  title=title1, template=TEMPLATE)
    fig1.update_xaxes(categoryorder="array", categoryarray=primary_classes)
    fig1.update_layout(yaxis_title=ytitle1)
    fig1.update_layout(xaxis_title=xtitle1)
    fig1.update_traces(hovertemplate=hovertempl1)
    graph1 = dcc.Graph(
        figure = fig1,
        className="border",
    )

    # Graph 2 : Overview of SCP article length, rating and mentions in other articles ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    # dropping unwanted rows
    ratings_df = df.dropna(subset=["rating"])
    ratings_df = ratings_df[ratings_df["rating"] > 0]
    # calculating article length
    ratings_df["length"]=ratings_df.apply(lambda row: len(row["text"]), axis=1)
    # setting anything else than the top 5 classes to "other" to avoid having too many categories
    top5classes = pd.DataFrame(ratings_df["class"].value_counts()).head(5).reset_index()["class"].tolist()
    is_top5class = ratings_df["class"].isin(top5classes)
    ratings_df.loc[-is_top5class, "class"] = "Other"
    
    if current_mode !=2:
        title2 = "Overview of SCP article length, rating and mentions in other articles"
    else:
        title2 = "Big egg"
        
    graph2 = dcc.Graph(
        figure=px.scatter(
            ratings_df.dropna(subset=["rating"]),
            x="length",
            y="mentions",
            size="rating",
            color="class",
            color_discrete_sequence=px.colors.qualitative.Bold,
            hover_name="code",
            animation_frame="series",
            hover_data = {"series":False},
            category_orders={"class": ["Neutralized", "Thaumiel", "Safe", "Euclid", "Keter", "Other"]},
            log_x=True,
            size_max=60,
            title= title2,
            template=TEMPLATE,
        ),
        className="border",
    )

    # Graph 3 : [Amount of black rectangles (█) per article] ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    black_df = df
    black_df["black rectangles"] = black_df.apply(lambda row: contains_count(row["text"], ["█"]), axis=1)
    topclasses = pd.DataFrame(df["class"].value_counts()).head(3).reset_index()
    tclist = topclasses["class"].tolist()
    tc_scps = black_df["class"].isin(tclist)
    black_df = black_df[tc_scps]

    if current_mode !=2:
        title3 = "Quantity of black rectangles (█ character) per article"
        ytitle3 = "black rectangles"
        xtitle3 = "class"
    else:
        title3 = "Quantity of brown eggs per carton"
        ytitle3 = "brown eggs"
        xtitle3 = "roundness"
        is_safe = (black_df["class"] == "Safe")
        is_euclid = (black_df["class"] == "Euclid")
        is_keter = (black_df["class"] == "Keter")
        black_df.loc[is_safe, "class"] = "Big round"
        black_df.loc[is_euclid, "class"] = "Round"
        black_df.loc[is_keter, "class"] = "Kind of round"
        
    fig3 = px.violin(
        black_df,
        y="black rectangles",
        x="class",
        color="series",
        color_discrete_sequence=px.colors.sequential.Plasma_r,
        box=True,
        points="all",
        hover_data={"code":True, "title":True, "class": False, "series": False},
        title=title3,
        template=TEMPLATE,
    )

    fig3.update_layout(yaxis_title=ytitle3)
    fig3.update_layout(xaxis_title=xtitle3)
    fig3.update_xaxes(categoryorder="array", categoryarray=primary_classes)
    
    graph3 = dcc.Graph(
        figure=fig3,
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
        dbc.Row(dbc.Col(html.Div(id="graphs"))),
        dbc.Row(dbc.Col(links))
    ],
    className="dbc p-4",
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True)