import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv"
    data = pd.read_csv(url)
    return data

data = load_data()

# Handle missing values in size-related columns
data["total_cases"] = data["total_cases"].fillna(0)  
data["total_deaths"] = data["total_deaths"].fillna(0)
data["total_vaccinations"] = data["total_vaccinations"].fillna(0)

# Sidebar filters
st.sidebar.title("Filters")
continent_filter = st.sidebar.multiselect(
    "Select Continents",
    options=data["continent"].dropna().unique(),
    default=data["continent"].dropna().unique()
)
metric_filter = st.sidebar.selectbox(
    "Select Metric to Visualize",
    options=["total_cases", "total_deaths", "total_vaccinations"],
    index=0
)

# Filter data based on sidebar inputs
filtered_data = data[data["continent"].isin(continent_filter)]

# Main app title
st.title("COVID-19 Global Dashboard")

# Display dataset summary
st.subheader("Dataset Overview")
st.write(f"Data includes {len(data)} countries.")
if st.checkbox("Show raw data"):
    st.write(filtered_data)

# Metric summary
st.subheader(f"Global {metric_filter.replace('_', ' ').title()} by Continent")
continent_summary = filtered_data.groupby("continent")[metric_filter].sum().reset_index()
fig_bar = px.bar(
    continent_summary,
    x="continent",
    y=metric_filter,
    color="continent",
    title=f"Total {metric_filter.replace('_', ' ').title()} by Continent",
)
st.plotly_chart(fig_bar)

# Map visualization
st.subheader(f"Geographic Distribution of {metric_filter.replace('_', ' ').title()}")
fig_map = px.scatter_geo(
    filtered_data,
    locations="iso_code",
    color="continent",
    hover_name="location",
    size=metric_filter, 
    projection="natural earth",
    title=f"{metric_filter.replace('_', ' ').title()} by Country",
)
st.plotly_chart(fig_map)

# Top 10 countries by selected metric
st.subheader(f"Top 10 Countries by {metric_filter.replace('_', ' ').title()}")
top_countries = filtered_data.nlargest(10, metric_filter)[["location", metric_filter]]
st.table(top_countries)

# Footer
st.markdown("---")
st.markdown("Data source: [Our World in Data](https://ourworldindata.org/coronavirus)")