import yfinance as yf
import pandas as pd
import pickle

# List of tickers
ticker_list = [
    "^GSPC",  # S&P 500 Index
    "CL=F",   # Crude Oil (WTI)
    "BZ=F",   # Brent Crude Oil
    "UNG",    # United States Natural Gas Fund
    "GC=F",   # Gold Futures
    "URA",    # Global X Uranium ETF
    "XLE"     # Energy Select Sector SPDR Fund
]

# Time period and interval 
start_date = "2022-11-29" # Period cannot exceed 730 days
end_date = "2024-11-27"
interval = "1h"

# Fetching data
ticker_intraday_prices = {}
for ticker in ticker_list:
    print(f"Downloading data for {ticker}...")
    try:
        ticker_intraday_prices[ticker] = yf.download(tickers=ticker, start=start_date, end=end_date, interval=interval)
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")

# Combine into a single DataFrame
all_data = pd.concat(ticker_intraday_prices, axis=1)

# Extract only the "Adj Close" column for each ticker
adj_close_data = all_data.xs('Adj Close', axis=1, level=1)

# Rename columns to match ticker names
adj_close_data.columns = [col[0] for col in adj_close_data.columns]

# Extrapolate NaN values using linear interpolation
adj_close_data = adj_close_data.interpolate(method='linear', limit_direction='both')

# Ensure the current datetime index is reset and added as a column
adj_close_data = adj_close_data.reset_index()

# Rename the column 'Datetime' to 'Date'
adj_close_data = adj_close_data.rename(columns={'Datetime': 'Time'})

# Set the row index to a simple integer-based index
adj_close_data.index = range(len(adj_close_data))

# Round to closest hour
adj_close_data['Time'] = pd.to_datetime(adj_close_data['Time']).dt.round('h')

# Convert 'Time' column in all DataFrames to naive datetime (remove timezone)
adj_close_data['Time'] = pd.to_datetime(adj_close_data['Time']).dt.tz_localize(None)

# Display the resulting DataFrame
print(adj_close_data.head())

adj_close_data.to_pickle("./Data/stock_prices.pkl")
