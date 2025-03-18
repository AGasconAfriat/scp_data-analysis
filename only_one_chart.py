import dash
from dash import dcc, html
import pandas as pd
import matplotlib.pyplot as plt
import math
import re
import plotly.graph_objects as go
import plotly.express as px

# Initialize Dash app
app = dash.Dash(__name__)

def get_class(text):
    x = re.findall(r"\\n (\w*) Class: (\w*) \\n", text)
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

df = pd.read_csv("scp6999.csv")

df["class type"] = df["text"].apply(get_class_type)
df["class"] = df["text"].apply(get_class_spec)
df["series"] = df["code"].apply(get_series)

primary_classes=["Safe", "Euclid", "Keter"]
primary_classes_df = df[df["class"].isin(primary_classes)]
class_counts = primary_classes_df.groupby(["class", "series"]).count().reset_index()

fig = px.histogram(class_counts, x="class", y="code", color="series", color_discrete_sequence=px.colors.sequential.Plasma_r, barmode="group",
                  title="Distribution of SCPs by containment class by series")
fig.update_xaxes(categoryorder="array", categoryarray=primary_classes)
fig.update_layout(yaxis_title="")
fig.update_traces(hovertemplate='Total SCPs: %{y}<extra></extra>')

app.layout = html.Div(children=[
    html.H1("SCP Containment Class Distribution"),
    dcc.Graph(id="scp_chart", figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)