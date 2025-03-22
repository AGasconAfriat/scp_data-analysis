from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import pandas as pd
import matplotlib.pyplot as plt
import math
import re
import plotly.graph_objects as go
import plotly.express as px
import random

def contains_count(string, elements):
    count = 0
    for element in elements:
        count += string.count(element)
    return count

def get_code_plus_title(code, title):
    return str(code) + ": " + str(title[1:-1])

pd.set_option('display.max_colwidth', None)

df = pd.read_csv("scp6999augmented.csv")
df["length"]=df.apply(lambda row: len(row["text"]), axis=1)
df["full title"]=df.apply(lambda row: get_code_plus_title(row["code"], row["title"]), axis=1)

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"
)

# modes
modes = {0: "Default mode", 1: "Antimemetic mode", 2: "Big egg"}

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])
app.title = "SCP Status"

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

def make_figures(current_mode, current_df):
    #if current_mode != 1:
    #    current_df = df #resets the df in case antimemetic mode was previously enabled
    # Graph 1 : Distribution of SCPs by containment class by series ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    primary_classes=["Safe", "Euclid", "Keter"]
    primary_classes_df = current_df[current_df["class"].isin(primary_classes)]
    if current_mode != 2:
        title1 = "Distribution of SCPs by containment class by series"
        ytitle1 = ""
        hovertempl1 = "Total SCPs: %{y}<extra></extra>"
        xtitle1 = "class"
        series_name = "series"
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
        primary_classes_df.rename(columns={"series": "yolk ph"}, inplace=True)
        series_name = "yolk ph"
    class_counts = primary_classes_df.groupby(["class", series_name]).count().reset_index()
    fig1 = px.histogram(class_counts, x="class", y="code", color=series_name, color_discrete_sequence=px.colors.sequential.Plasma_r, barmode="group",
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
    ratings_df = current_df.dropna(subset=["rating"])
    ratings_df = ratings_df[ratings_df["rating"] > 0]
    # calculating article length
    ratings_df["length"]=ratings_df.apply(lambda row: len(row["text"]), axis=1)
    # setting anything else than the top 5 classes to "other" to avoid having too many categories
    top5classes = pd.DataFrame(ratings_df["class"].value_counts()).head(5).reset_index()["class"].tolist()
    is_top5class = ratings_df["class"].isin(top5classes)
    ratings_df.loc[-is_top5class, "class"] = "Other"
    
    if current_mode !=2:
        title2 = "Overview of SCP article length, rating and mentions in other articles"
        xtitle2 = "length (in characters)"
        ytitle2 = "mentions"
        hover_data2 = {"series": False}
    else:
        title2 = "Big egg"
        xtitle2 = "bigness"
        ytitle2 = "yolk"
        is_safe = (ratings_df["class"] == "Safe")
        is_euclid = (ratings_df["class"] == "Euclid")
        is_keter = (ratings_df["class"] == "Keter")
        is_neut = (ratings_df["class"] == "Neutralized")
        is_thau = (ratings_df["class"] == "Thaumiel")
        ratings_df.loc[is_safe, "class"] = "Big round"
        ratings_df.loc[is_euclid, "class"] = "Round"
        ratings_df.loc[is_keter, "class"] = "Kind of round"
        ratings_df.loc[is_neut, "class"] = "Omelet"
        ratings_df.loc[is_thau, "class"] = "Carton"
        ratings_df["full title"] = "SCP-Big egg"
        hover_data2 = {"series": False}

    fig2 = px.scatter(
        ratings_df.dropna(subset=["rating"]),
        x="length",
        y="mentions",
        size="rating",
        color="class",
        color_discrete_sequence=px.colors.qualitative.Bold,
        hover_name="full title",
        animation_frame="series",
        hover_data = hover_data2,
        category_orders={"class": ["Neutralized", "Thaumiel", "Safe", "Euclid", "Keter", "Omelet", "Carton", "Big round", "Round", "Kind of round", "Other"]},
        log_x=True,
        size_max=60,
        title= title2,
        template=TEMPLATE
    )
    fig2.update_layout(xaxis_title=xtitle2)
    fig2.update_layout(yaxis_title=ytitle2)
    graph2 = dcc.Graph(
        figure=fig2,
        className="border",
    )

    # Graph 3 : [Amount of black rectangles (█) per article] ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    black_df = current_df
    black_df["black rectangles"] = black_df.apply(lambda row: contains_count(row["text"], ["█"]), axis=1)
    topclasses = pd.DataFrame(current_df["class"].value_counts()).head(3).reset_index()
    tclist = topclasses["class"].tolist()
    tc_scps = black_df["class"].isin(tclist)
    black_df = black_df[tc_scps]

    if current_mode !=2:
        title3 = "Quantity of black rectangles (█ character) per article"
        xtitle3 = "class"
        ycol3 = "black rectangles"
        series_name = "series"
    else:
        title3 = "Quantity of brown eggs per carton"
        xtitle3 = "roundness"
        is_safe = (black_df["class"] == "Safe")
        is_euclid = (black_df["class"] == "Euclid")
        is_keter = (black_df["class"] == "Keter")
        black_df.loc[is_safe, "class"] = "Big round"
        black_df.loc[is_euclid, "class"] = "Round"
        black_df.loc[is_keter, "class"] = "Kind of round"
        black_df.rename(columns={"black rectangles": "brown eggs", "series": "yolk ph"}, inplace=True)
        black_df["full title"] = "SCP-Big egg"
        ycol3 = "brown eggs"
        series_name = "yolk ph"
        
    fig3 = px.violin(
        black_df,
        y=ycol3,
        x="class",
        color=series_name,
        color_discrete_sequence=px.colors.sequential.Plasma_r,
        box=True,
        points="all",
        hover_name="full title",
        hover_data={"class": False, series_name: False},
        title=title3,
        template=TEMPLATE,
    )
    fig3.update_layout(xaxis_title=xtitle3)
    fig3.update_xaxes(categoryorder="array", categoryarray=primary_classes)
    
    graph3 = dcc.Graph(
        figure=fig3,
        className="border",
    )

    # Graph 4 : Top 5 ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    top_rated_df = current_df.sort_values(by="rating", ascending=False).head()[["full title", "rating"]]
    top_rated_df["rank"] = range(1, len(top_rated_df) + 1)
    top_rated_df.rename(columns={"rating": "amount", "full title": "title"}, inplace=True)
    top_rated_df["amount"] = top_rated_df["amount"]//10
    top_rated_df["category"] = "rating (tens of points)"
    
    most_refs_df = df.sort_values(by="mentions", ascending=False).head()[["full title", "mentions"]]
    most_refs_df["rank"] = range(1, len(top_rated_df) + 1)
    most_refs_df.rename(columns={"mentions": "amount", "full title": "title"}, inplace=True)
    most_refs_df["category"] = "mentions"
    
    longest_df = current_df.sort_values(by="length", ascending=False).head()[["full title", "length"]]
    longest_df["rank"] = range(1, len(top_rated_df) + 1)
    longest_df.rename(columns={"length": "amount"}, inplace=True)
    longest_df["amount"] = longest_df["amount"]//100
    longest_df["category"] = "article length (hundreds of characters)"
    longest_df.rename(columns={"full title": "title"}, inplace=True)

    if current_mode == 2:
        top_rated_df["category"] = "taste rating"
        most_refs_df["category"] = "culinary uses"
        longest_df["category"] = "mass (grams)"
        
    top5_df = pd.DataFrame(columns=['category', 'title', 'amount', 'rank'])
    top5_df = pd.concat([top5_df, top_rated_df, longest_df, most_refs_df], ignore_index=True)

    if current_mode == 2:
        top5_df["title"] = "SCP-Big egg"
        
    fig4 = px.bar(top5_df, x="category", y="amount", color="rank", color_discrete_sequence=px.colors.sequential.Plasma_r, barmode="group",
                      title="Top 5", hover_name="title", template=TEMPLATE)
    
    graph4 = dcc.Graph(
        figure=fig4,
        className="border",
    )

    return [
        dbc.Row([dbc.Col(graph1, lg=6), dbc.Col(graph2, lg=6)]),
        dbc.Row([dbc.Col(graph3, lg=6), dbc.Col(graph4, lg=6)], className="mt-4"),
    ]

@app.callback(
    Output("graphs", "children"),
    [Input(component_id='dashboard-mode', component_property='value'),
     Input('interval-component', 'n_intervals')]
)
def update_dashboard(current_mode, n):
    if "current_df" not in locals():
        current_df = df
    if current_mode != 1: #default or big egg mode
        if ("last_mode" not in locals()) or (last_mode != current_mode):
            last_mode = current_mode
            last_graphs = make_figures(current_mode, df)
        return last_graphs
    else: #antimemetic mode
        to_drop = random.sample(list(current_df.index), math.ceil(len(current_df)/2))
        current_df.drop(to_drop)
        return make_figures(current_mode, current_df)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(mode_select, lg=2)
            ],
        ),
        dbc.Row(dbc.Col(html.Div(id="graphs"))),
        dbc.Row(dbc.Col(links)),
        dcc.Interval(
            id='interval-component',
            interval=10*1000,  # in milliseconds
            n_intervals=0
        )
    ],
    className="dbc p-4",
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True)