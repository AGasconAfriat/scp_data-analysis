#import kagglehub
import pandas as pd
import matplotlib.pyplot as plt
import math
import re

pd.set_option('display.max_colwidth', None)

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
def count_mentions(code): #counts mentions of a SCP in the text column of every row except its own
    links_pattern = r"« \w+-\d+ [|] \w+-\d+ [|] \w+-\d+ »"
    mentions = 0
    temp_df = df[df['code'] != code] # remove the SCP's own article
    for scp_text in temp_df['text']:
        scp_text = re.sub(links_pattern, "", scp_text)
        mentions = mentions + scp_text.count(code)
    return mentions

#path = kagglehub.dataset_download("czzzzzzz/scp1to7")
#df = pd.read_csv(f"{path}/scp6999.csv")
df = pd.read_csv("scp6999.csv")

# Adding columns
df["class type"] = df["text"].apply(get_class_type)
df["class"] = df["text"].apply(get_class_spec)
df["series"] = df["code"].apply(get_series)
df["mentions"] = df["code"].apply(count_mentions)

# Removing rows corresponding to unassigned SCP codes
df = df[df["state"]!="deleted"]

df.to_csv("scp6999augmented.csv")