import pandas as pd
import pickle


# HOURLY WEATHER DATA
# File path for the weather data
file_path_weather = "./Data/Raw/Helsinki Malmi lentokenttä_ 1.1.2021 - 25.11.2024.xlsx"  # Get latest from: https://en.ilmatieteenlaitos.fi/download-observations
# Read the weather data, assuming proper headers start at the top
data_weather = pd.read_excel(file_path_weather)


# Combine year, month, day, and time columns into a single timestamp
data_weather['Time'] = pd.to_datetime(
    data_weather[['Vuosi', 'Kuukausi', 'Päivä']].astype(str).agg('-'.join, axis=1) + ' ' + data_weather['Aika [Paikallinen aika]']
)

# Select all specified columns and rename them for better readability
data_weather = data_weather[[
    'Time',
    'Ilmanpaineen keskiarvo [hPa]',
    'Lämpötilan keskiarvo [°C]',
    'Keskituulen nopeus [m/s]',
    'Kovin keskituulen nopeus [m/s]',
    'Tuulen suunnan keskiarvo [°]',
    'Tunnin sademäärä [mm]',
    'Kovin puuska [m/s]',
    'Suhteellisen kosteuden keskiarvo [%]',
    'Alin lämpötila [°C]',
    'Ylin lämpötila [°C]'
]].rename(columns={
    'Ilmanpaineen keskiarvo [hPa]': 'Pressure (hPa)',
    'Lämpötilan keskiarvo [°C]': 'Temperature (°C)',
    'Keskituulen nopeus [m/s]': 'Avg Wind Speed (m/s)',
    'Kovin keskituulen nopeus [m/s]': 'Max Avg Wind Speed (m/s)',
    'Tuulen suunnan keskiarvo [°]': 'Avg Wind Direction (°)',
    'Tunnin sademäärä [mm]': 'Rainfall (mm)',
    'Kovin puuska [m/s]': 'Max Gust (m/s)',
    'Suhteellisen kosteuden keskiarvo [%]': 'Humidity (%)',
    'Alin lämpötila [°C]': 'Min Temperature (°C)',
    'Ylin lämpötila [°C]': 'Max Temperature (°C)'
})

# Add extra useful variables
data_weather['Hour of Day'] = data_weather['Time'].dt.hour
data_weather['Day of Week'] = data_weather['Time'].dt.dayofweek
data_weather['Month'] = data_weather['Time'].dt.month


# Convert numerical columns to numeric, replacing commas with dots if needed
for col in [
    'Pressure (hPa)', 'Temperature (°C)', 'Avg Wind Speed (m/s)',
    'Max Avg Wind Speed (m/s)', 'Avg Wind Direction (°)', 'Rainfall (mm)',
    'Max Gust (m/s)', 'Humidity (%)', 'Min Temperature (°C)', 'Max Temperature (°C)',
    'Hour of Day'
]:
    data_weather[col] = pd.to_numeric(data_weather[col].astype(str).str.replace(',', '.'), errors='coerce')



# Drop columns where all values are NaN
data_weather = data_weather.dropna(axis=1, how='all')
# Drop rows where any value is NaN
data_weather = data_weather.dropna(axis=0, how='any')

# Round time to closest hour
data_weather['Time'] = pd.to_datetime(data_weather['Time']).dt.round('h')

data_weather.to_pickle("./Data/weather_data.pkl")

# Display the resulting DataFrame
print(data_weather.head())

