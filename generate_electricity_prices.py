import pandas as pd
import pickle

# HOURLY ELECTRICITY PRICING
# Load the Excel file
file_path = "./Data/Raw/electricity-price-010121-271124.xlsx"  # Download latest by pressing 'lataa' at https://porssisahko.net/tilastot
hourly_electricity_prices = pd.read_excel(file_path,  skiprows=4)

# Rename columns for easier handling
hourly_electricity_prices.columns = ["Time", "Price"]

# Convert 'Time' column to datetime and 'Price' to numeric
hourly_electricity_prices['Time'] = pd.to_datetime(hourly_electricity_prices['Time'], format='%d/%m/%Y %H:%M:%S')
hourly_electricity_prices['Price'] = pd.to_numeric(hourly_electricity_prices['Price'], errors='coerce')

# Round time to closest hour
hourly_electricity_prices['Time'] = pd.to_datetime(hourly_electricity_prices['Time']).dt.round('h')

# Save data
hourly_electricity_prices.to_pickle("./Data/electricity_prices.pkl")

print(hourly_electricity_prices.head())