import streamlit as st
import requests
import pandas as pd

st.title("Global Health Tracker")

# Fetch data from World Bank (Life Expectancy)
url = "https://api.worldbank.org/v2/country/all/indicator/SP.DYN.LE00.IN?format=json&per_page=20000"
data = requests.get(url).json()[1]

# Flatten nested JSON and select columns
df = pd.json_normalize(data)
df = df[['country.value', 'date', 'value']]
df.columns = ['Country', 'Year', 'Life_Expectancy']

# Simple filter and chart
selected_country = st.selectbox("Select Country", sorted(df['Country'].unique()))
filtered = df[df['Country'] == selected_country]

st.line_chart(filtered.set_index('Year')['Life_Expectancy'])