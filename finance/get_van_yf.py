import datetime as dt

import yfinance as yf

end_date = dt.datetime.now() + dt.timedelta(days=1)
days = 90
start_date = end_date - dt.timedelta(days=days)

ticker = "0P0000TKZI.L"

ticker_name = yf.Ticker(ticker).info["longName"]

df = yf.download(ticker, start_date, end_date)
df = df[["Close"]]

# divide Close by 100 to get the price in GBP and round to 2 decimal places
df["Close"] = round(df["Close"] / 100, 2)

# get the max, min and average values for the last 90 days
max_value = df["Close"].max()
min_value = df["Close"].min()
avg_value = round(df["Close"].mean(), 2)

# order the dataframe by date descending
df = df.sort_values(by="Date", ascending=False)

print(f"\n\n---------------{ticker_name}---------------\n")
print(df)

print(f"\n\nStats for past {days} days:")
print(f"Max: {max_value}")
print(f"Min: {min_value}")
print(f"Avg: {avg_value}")
