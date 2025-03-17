# scp_data-analysis

## Introduction

The SCP Foundation is a fictional organization at the center of a collaborative wiki-based creative project, the [SCP Wiki](https://scp-wiki.wikidot.com/). Within the project's fictional universe, the Foundation is a secret organization charged with studying and containing various anomalous objects and phenomena, called "SCPs".

Many of the projet's fictional works are mock confidential scientific reports documenting various SCPs and their containment procedures. While these reports are typically written in a dry, academic writing style, many of them are quite dark and/or humorous.

Famous examples of SCPs include:

- [SCP-3008](https://scp-wiki.wikidot.com/scp-3008), an abandoned IKEA store containing a pocket dimension of seemingly infinite proportions housing faceless creatures wearing employee uniforms as well as unlucky humans who, having found their way into the anomaly, are unable to find an exit,
- [SCP-294](https://scp-wiki.wikidot.com/scp-294), a coffee machine capable of producing any liquid requested by typing its name into the machine’s English QWERTY keyboard after having inserted 0.50 USD into the coin slot, and
- [SCP-173](https://scp-wiki.wikidot.com/scp-173), a sculpture composed of concrete and rebar who violently attacks people unless it is visually observes

## Project Overview

This project contains files to scrape PWHL player data, save it in a CSV file and display it in the form of a dashboard.

TODO ![The upper part of a dashboard titled PWHL Player Statistics, featuring a season selection dropdown menu and three charts.](visual_samples/currentseason_top.png)

## Files

### Files Showing the Development Process

TODO

* `skater_stats_to_csv.ipynb`: A notebook showing how to create a dataset from PWHL skater statistics and save it as a CSV file.
* `skater_stats.csv`: A sample CSV file containing PWHL skater statistics.
* `visualizations.ipynb`: A notebook showing how to create different types of visualizations based on skater statistics.

### Files Showing the Dashboard

TODO

The `visual_samples` folder contains screen captures of the dashboard.

### Files To Run the Dashboard

TODO

* `step1_get_stats.py`: A script to scrape the data and save it into a CSV file.
* `full_stats.csv`: A CSV file generated using `step1_get_stats.py`.
* `step2_run_dashboard.py`: A script to run the interactive dashboard.

## Script Dependencies

TODO

The scripts require Python to be installed.

To run the scripts (`.py` files), need certain packages installed. For example, I had to run the following commands in command line/terminal before the scripts.

```
pip install setuptools
python -m pip 
python -m pip install packaging
python -m pip install pandas dash
python -m pip install selenium
pip install httpx==0.20 dash plotly
```

An easy way to see if you are lacking anything is to try to run the script, then install the appropriate package if you get an error message about missing dependencies.

`step1_get_stats.py` needs a WebDriver to be installed. Consult [the supported browsers section of the Selenium downloads page](https://www.selenium.dev/downloads/#supported-browsers) for more information. If not using Edge, update line 24 of `step1_get_stats.py` with the appropriate WebDriver.

## Running a Python script

TODO

To run a script, use the following command:

```
python <path>/<filename>
```

## Running the Scripts and Accessing the Dashboard

TODO

First, run `step1_get_stats.py`. WebDriver will open and close multiple webpages displaying PWHL player statistics. Wait for the script to end. It will output "Step 1 complete."

**NOTE 1**: It is normal for the script to take a while as it needs to open a large number of webpages (46 at time of writing), waiting for each to load the table, then scraping the data.

**NOTE 2**: You may see a list of WebDriver-related warnings and errors in the console. They should not prevent the script from completing.

Then, run `step2_run_dashboard.py`. Its output should specify which port it is running on.

Example with port 8050:

```
 * Serving Flask app 'step2_run_dashboard'
 * Debug mode: off
 * Running on http://127.0.0.1:8050
```

## TODO

TODO

Not yet implemented:
- Make the dashboard responsive (display charts above each other instead of next to each other on a smaller screen)