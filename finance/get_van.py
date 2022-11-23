from bs4 import BeautifulSoup
import pandas as pd


url = "https://markets.ft.com/data/funds/tearsheet/historical?s=GB00B3ZHN960:GBP"

df = pd.read_html(url, flavor="bs4")[0]

# select columns we want
df = df[["Date", "High"]]

df['Date'] = df['Date'].str.split(',')
df['Date'] = df['Date'].apply(lambda x: ','.join([x[0], x[1], x[4]]))
print(df)





