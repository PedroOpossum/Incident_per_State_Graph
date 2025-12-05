import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd;
import requests
from io import StringIO


stateInput = input("Enter the state you want: ")


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    }


url = f"https://www.bls.gov/iif/state-data/fatal-occupational-injuries-in-{stateInput}-2023.htm"

try:
    injuryTable = requests.get(url, headers=headers, timeout = 5)
    data = pd.read_html(StringIO(injuryTable.text))
    df = data[0]

    print(df.head())

except requests.exceptions.Timeout:
    print("\nERROR: The request timed out.")
except requests.exceptions.ConnectionError:
    print("\nERROR: Network connection problem.")


