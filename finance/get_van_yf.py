import datetime as dt

import yfinance as yf

end_date = dt.datetime.now() + dt.timedelta(days=1)
start_date = end_date - dt.timedelta(days=30)

ticker = "0P0000TKZI.L"

ticker_name = yf.Ticker(ticker).info["longName"]

df = yf.download(ticker, start_date, end_date)
df = df[["Close"]]

# divide Close by 100 to get the price in GBP and round to 2 decimal places
df["Close"] = round(df["Close"] / 100, 2)

# order the dataframe by date descending
df = df.sort_values(by="Date", ascending=False)

print(f"\n\n---------------{ticker_name}---------------")
print(df)
