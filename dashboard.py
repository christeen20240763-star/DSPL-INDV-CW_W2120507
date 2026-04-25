import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

df = pd.read_excel("/Users/delphina/Downloads/YEAR 02/DSPL/DSPL 2/DSPL CW 2/cleaned_what_a_waste_data.xlsx")

# ---- SIDEBAR ----
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df['region'].unique(),
    default=df['region'].unique()  # all selected by default
)

income = st.sidebar.multiselect(
    "Select Income Group",
    options=df['income_group'].unique(),
    default=df['income_group'].unique()
)

# Filter the dataframe based on sidebar selection
df = df[df['region'].isin(region) & df['income_group'].isin(income)]


st.title("Global Waste Dashboard")



st.markdown("""
### Exploring global waste generation, income levels, regional patterns, and sustainability gaps.
""")

# KPI
st.header("Key Insights")

avg_waste = df["msw_kg_per_capita_per_day"].mean()
top = df.loc[df["msw_kg_per_capita_per_day"].idxmax()]
low = df.loc[df["msw_kg_per_capita_per_day"].idxmin()]

col1, col2, col3 = st.columns(3)

col1.metric("Average Waste (kg/day)", round(avg_waste, 2))
col2.write("**Highest Waste Country**")
col2.write(f"{top['country_name']} ({top['msw_kg_per_capita_per_day']:.2f} kg/day)")
col3.write("**Lowest Waste Country**")
col3.write(f"{low['country_name']} ({low['msw_kg_per_capita_per_day']:.2f} kg/day)")

# Income chart
st.subheader("Waste by Income Group")

income_data = df.groupby("income_group")["msw_kg_per_capita_per_day"].mean().sort_values()

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(income_data.index, income_data.values)
ax.set_xlabel("Waste per capita (kg/day)")
ax.set_ylabel("Income Group")
st.pyplot(fig)

# Region chart
st.subheader("Waste by Region")

region_data = df.groupby("region")["msw_kg_per_capita_per_day"].mean().sort_values()

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(region_data.index, region_data.values)
ax.set_xlabel("Waste per capita (kg/day)")
ax.set_ylabel("Region")
st.pyplot(fig)

# Top 10 countries
st.subheader("Top 10 Waste Generating Countries")

top10 = df.nlargest(10, "msw_tonnes_per_year")

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top10["country_name"], top10["msw_tonnes_per_year"])
ax.set_xlabel("Total Waste (tonnes/year)")
ax.set_ylabel("Country")
st.pyplot(fig)

# Waste composition
st.subheader("Waste Composition")

labels = ["Food", "Paper", "Plastic"]
values = [
    df["composition_food%_weight_msw"].mean(),
    df["composition_paper_cardboard%_weight_msw"].mean(),
    df["composition_plastic%_weight_msw"].mean()
]

fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(values, labels=labels, autopct="%1.1f%%")
st.pyplot(fig)


import plotly.express as px

st.subheader("🌍 Global Waste Map")

# Dropdown for metric selection
map_metric = st.selectbox(
    "Select metric to display on the map",
    options=[
        "Total waste generated (t/year)",
        "Waste per capita (kg/capita/day)",
        "Collection coverage (%)"
    ]
)

# Map selection to actual column names
map_column = {
    "Total waste generated (t/year)": "msw_tonnes_per_year",
    "Waste per capita (kg/capita/day)": "msw_kg_per_capita_per_day",
    "Collection coverage (%)": "collection_coverage"
}[map_metric]

# Prepare data
map_df = df[["country_name", map_column]].dropna()

# Create choropleth map
fig_map = px.choropleth(
    map_df,
    locations="country_name",
    locationmode="country names",
    color=map_column,
    hover_name="country_name",
    title=f"Global Map of {map_metric}",
    
    # 🌱 nicer color scale
    color_continuous_scale="YlGn"
)

# Clean layout
fig_map.update_layout(
    margin=dict(l=0, r=0, t=50, b=0)
)

# Show in Streamlit
st.plotly_chart(fig_map, use_container_width=True)