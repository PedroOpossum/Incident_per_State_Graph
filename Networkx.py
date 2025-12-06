import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd;
import requests
from io import StringIO


urlState = "https://www.bls.gov/iif/state-data/archive.htm#NJ"


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

    for stateLoop in states:
        urlInjury = f"https://www.bls.gov/iif/state-data/fatal-occupational-injuries-in-{stateLoop}-2023.htm"
        print(urlInjury)



except requests.exceptions.Timeout:
    print("\nERROR: The request timed out.")
except requests.exceptions.ConnectionError:
    print("\nERROR: Network connection problem.")


