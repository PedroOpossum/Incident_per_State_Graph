import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd;
import pyarrow as pa;
import pyarrow.parquet as pq
import requests

url = "https://www.bls.gov/iif/state-data/fatal-occupational-injuries-in-texas-2023.htm"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
data = pd.read_html(response.text)
df = data[0]
print(df.head())