import pandas as pd
import pickle


electricity_prices = pd.read_pickle("./Data/electricity_prices.pkl")
stock_prices = pd.read_pickle("./Data/stock_prices.pkl")
weather_data = pd.read_pickle("./Data/weather_data.pkl")


print(electricity_prices.columns)
print(stock_prices.columns)
print(weather_data.columns)

spot_pricing_dataset = pd.merge(electricity_prices, weather_data, on='Time', how='inner')
spot_pricing_dataset = pd.merge(spot_pricing_dataset, stock_prices, on='Time', how='inner')

# Compute correlation matrix
correlation_matrix = spot_pricing_dataset.corr()

# Extract correlation of weather variables with 'Price'
correlation_with_price = correlation_matrix['Price'].sort_values(ascending=False)

# Display the correlation values
print("Correlation of weather variables with electricity price:")
print(correlation_with_price)

