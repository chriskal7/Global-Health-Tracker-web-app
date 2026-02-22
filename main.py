import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Global Health Tracker", layout="wide")
st.title("🌍 Global Health Tracker")

@st.cache_data
def load_data():
    url = "https://api.worldbank.org/v2/country/all/indicator/SP.DYN.LE00.IN?format=json&per_page=20000"
    data = requests.get(url).json()[1] # jsonify
    df = pd.json_normalize(data)[['country.value', 'date', 'value']] # Normalize
    df.columns = ['Country', 'Year', 'Life_Expectancy'] # Rename columns
    df = df.dropna().sort_values('Year') # Remove missing values
    df['Year'] = df['Year'].astype(int)
    return df

def get_country_info(name):
    # Fetch flag and population
    res = requests.get(f"https://restcountries.com/v3.1/name/{name}?fullText=true")
    if res.status_code == 200:
        return res.json()[0]
    else:
        return None

df = load_data()
selected_country = st.sidebar.selectbox("Country", sorted(df['Country'].unique()))

col1, col2 = st.columns([1, 3])
info = get_country_info(selected_country)

with col1:
    if info:
        st.image(info["flags"]["png"], width=200)
        st.metric("Population", f"{info['population']:,}")
        st.write(f"**Region:** {info['region']}")
    else:
        st.write(f"Region not found")

with col2:
    filtered = df[df['Country'] == selected_country]
    st.line_chart(filtered.set_index('Year')['Life_Expectancy'])
    st.write(f"Peak life expectancy for {selected_country}: {int(filtered['Life_Expectancy'].max())}")