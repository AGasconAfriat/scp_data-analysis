import pandas as pd
import matplotlib.pyplot as plt
import math
import re

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

df = pd.read_csv("scp6999.csv")

df["class type"] = df["text"].apply(get_class_type)
df["class"] = df["text"].apply(get_class_spec)
df["series"] = df["code"].apply(get_series)

df.to_csv("scp6999augmented.csv")