import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_table(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    tables = pd.read_html(str(soup))
    return tables
