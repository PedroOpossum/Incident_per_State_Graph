import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd;
import requests
from io import StringIO


urlState = "https://www.bls.gov/iif/state-data/archive.htm#NJ"

Yearinput = input("Enter the year you want to view between 2023-2011: " )

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    }


try:
    stateTable = requests.get(urlState, headers=headers, timeout = 5)
    data = pd.read_html(StringIO(stateTable.text))
    df = data[0]
    df = df[["State", "Fatal Injury Counts"]]


    states = (
        df["State"]
        .str.lower()
        .iloc[1:]
        .str.replace(" ", "-")
        .tolist()
    )

    #New York state has different URL so it needs to be changed

    for stateLoop in states:
        urlInjury = f"https://www.bls.gov/iif/state-data/fatal-occupational-injuries-in-{stateLoop}-{Yearinput}.htm"
        injuryTable = requests.get(urlInjury, headers=headers, timeout = 5)
        tables = pd.read_html(StringIO(injuryTable.text))
        df = tables[0]

        if "Year" in df.columns:
            print(f"{stateLoop}: N/A")
            continue

        totalInjuries = df.iloc[0, 1]
        print(f"{stateLoop}: {totalInjuries}")



except requests.exceptions.Timeout:
    print("\nERROR: The request timed out.")
except requests.exceptions.ConnectionError:
    print("\nERROR: Network connection problem.")


