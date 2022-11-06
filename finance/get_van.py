from bs4 import BeautifulSoup
import pandas as pd


url = "https://markets.ft.com/data/funds/tearsheet/historical?s=GB00B3ZHN960:GBP"

df = pd.read_html(url, flavor="bs4")[0]
print(df)





