Global Health Tracker - Resilient Data Pipeline

An interactive dashboard built with Python and Streamlit that visualizes global life expectancy trends using real-time data from World Bank API.

Key Engineering Features
-Self-Healing Data Pipeline: Implemented a dual-layer caching system. The app automatically creates a local .csv backup upon a successful API call to ensure 100% uptime, even if the World Bank API is offline.
-Advanced Analytics: Integrated Plotly for interactive time-series analysis, including OLS Regression trendlines to identify long-term health patterns.
-API Integration: Consumes and normalizes complex JSON data from the World Bank REST API and metadata (flags/population) from RestCountries API.
-Performance Optimized: Leveraged @st.cache_data to minimize network overhead and provide a smooth user experience.

Tech Stack
-Backend: Python 3.x
-Data: Pandas, Requests, Statsmodels
-Frontend/Deployment: Streamlit
-Visualization: Plotly Express
