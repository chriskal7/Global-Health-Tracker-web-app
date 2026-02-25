import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os


st.set_page_config(page_title="Global Health Tracker", layout="wide")
st.title("🌍 Global Health Tracker")


@st.cache_data
def load_data():
    url = "https://api.worldbank.org/v2/country/all/indicator/SP.DYN.LE00.IN?format=json&per_page=20000"

    try:
        # Fetch data from World Bank API
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()[1]  # jsonify
        df = pd.json_normalize(data)[['country.value', 'date', 'value']]  # Normalize

        # Self-healing: Update local backup with fresh data
        df.to_csv("health_data_backup.csv", index=False)  # Write to backup csv
        st.sidebar.success("✅ Data synced from Live API")

    except:
        # Fallback mechanism: check if backup exists
        if os.path.exists("health_data_backup.csv"):
            st.warning("⚠️ API is offline. Loading cached local data...")
            df = pd.read_csv("health_data_backup.csv")
        else:
            # Emergency exit if both API and Backup fail
            st.error("❌ Critical Error: No data source available. Please try again later.")
            return pd.DataFrame(columns=['Country', 'Year', 'Life_Expectancy'])

    df.columns = ['Country', 'Year', 'Life_Expectancy']  # Rename columns
    df = df.dropna().sort_values('Year')  # Remove missing values
    df['Year'] = df['Year'].astype(int)  # Convert Year values to int
    return df


def get_country_info(name):
    # Fetch flag and population
    try:
        res = requests.get(f"https://restcountries.com/v3.1/name/{name}?fullText=true", timeout=5)
        if res.status_code == 200:
            return res.json()[0]
    except:
        return None


df = load_data()

# Ensure we have data before rendering the UI
if not df.empty:
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

        if not filtered.empty:
            # Create interactive Plotly chart
            fig = px.scatter(filtered, x='Year', y='Life_Expectancy',
                             title=f"Life Expectancy Trend in {selected_country}",
                             template="plotly_white",
                             trendline="ols",
                             trendline_color_override="red")

            fig.update_traces(mode='lines+markers')  # Connect scatterplot points into px.line

            st.plotly_chart(fig, width='stretch')

            # Analytical Insight
            max_val = filtered['Life_Expectancy'].max()
            peak_year = filtered[filtered['Life_Expectancy'] == max_val]['Year'].values[0]

            st.success(
                f"📈 **Analytical Insight:** {selected_country} reached its peak life expectancy of **{max_val:.1f} "
                f"years** in **{peak_year}**.")
else:
    st.info("Please check your internet connection and refresh to initialize the system.")