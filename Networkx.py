import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd;
import requests
from io import StringIO
from bs4 import BeautifulSoup

urlState = "https://www.bls.gov/iif/state-data/archive.htm#NJ"

Yearinput = input("Enter the year you want to view between 2023-2020: " ).strip()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    }


try:

    
    stateTable = requests.get(urlState, headers=headers, timeout = 5)
    data = pd.read_html(StringIO(stateTable.text))
    df = data[0]
    df = df[["State"]]


    states = (
        df["State"]
        .str.lower()

        #Skips "all participating states" row
        .iloc[1:]
        
        #The URL doesn't work for new york state, so we have to rename it, plus remove New York city since it isnt a state
        .replace({"new york state": "new york state including new york city", "new york city": pd.NA}) 

        # remove the NaN (NYC)
        .dropna()  

        #Converts it into a URL
        .str.replace(" ", "-")
        .tolist()
    )


    for stateLoop in states:
        urlInjury = f"https://www.bls.gov/iif/state-data/fatal-occupational-injuries-in-{stateLoop}-{Yearinput}.htm"
        injuryTable = requests.get(urlInjury, headers=headers, timeout = 5)
        tables = pd.read_html(StringIO(injuryTable.text))
        df = tables[0]

        #If the page doesn't exists it goes to https://www.bls.gov/iif/, where it displays "year" in the table. 
        if "Year" in df.columns:
            print(f"{stateLoop}: N/A")
            continue

        #Grabs the total fatal injuries from each state
        totalInjuries = df.iloc[0, 1]
        print(f"{stateLoop}: {totalInjuries}")



except requests.exceptions.Timeout:
    print("\nERROR: The request timed out.")
except requests.exceptions.ConnectionError:
    print("\nERROR: Network connection problem.")


