import datetime as dt

import yfinance as yf


def display_ticker_info(ticker):

    days = 90
    start_date = dt.datetime.now() - dt.timedelta(days=days)
    end_date = dt.datetime.now()

    # get long name of ticker
    ticker_info = yf.Ticker(ticker)
    if ticker_info.info:
        ticker_name = ticker_info.info.get("longName", "Ticker long name not available")
    else:
        ticker_name = "Error getting ticker info"

    df = yf.download(ticker, start_date, end_date)
    df = df.loc[:, ["Close"]]

    # divide Close by 100 to get the price in GBP and round to 2 decimal places
    df["Close"] = round(df["Close"] / 100, 2)

    # get the max, min and average values for the last 90 days
    max_value = df["Close"].max()
    min_value = df["Close"].min()
    avg_value = round(df["Close"].mean(), 2)

    # get the current value
    current_value = df["Close"].iloc[-1]

    # calculate percentage change from current value to value 90 days ago
    percentage_change = round(
        (current_value - df["Close"].iloc[0]) / df["Close"].iloc[0] * 100, 2
    )

    # order the dataframe by date descending
    df = df.sort_values(by="Date", ascending=False)

    print(f"\n\n---------------{ticker_name}---------------\n")
    print(df.head())
    print(df.tail())

    print(f"\n\nStats for past {days} days:")
    print(f"Max: {max_value}")
    print(f"Min: {min_value}")
    print(f"Avg: {avg_value}")
    print(f"Current: {current_value}")
    print(f"Percentage change from {days} days ago: {percentage_change}%")


tickers = ("0P0000TKZI.L", "0P0000TKZK.L")
for ticker_code in tickers:
    display_ticker_info(ticker_code)
