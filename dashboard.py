import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

df = pd.read_excel("/Users/delphina/Downloads/YEAR 02/DSPL/DSPL 2/DSPL CW 2/cleaned_what_a_waste_data.xlsx")

# ---- SIDEBAR ----
st.sidebar.title("🌍 Global Waste Dashboard")
st.sidebar.markdown("---")  # adds a divider line

st.sidebar.header("Filters")

year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df['year_reported'].unique()),
    default=sorted(df['year_reported'].unique())
)

region = st.sidebar.multiselect(
    "Select Region",
    options=df['region'].unique(),
    default=df['region'].unique()
)

income = st.sidebar.multiselect(
    "Select Income Group",
    options=df['income_group'].unique(),
    default=df['income_group'].unique()
)

# Filter dataframe
df = df[df['region'].isin(region) & 
        df['income_group'].isin(income) & 
        df['year_reported'].isin(year)]


st.title("Global Waste Dashboard")



st.markdown("""
### Exploring global waste generation, income levels, regional patterns, and sustainability gaps.
""")

#KPI cards

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_waste = df['msw_kg_per_capita_per_day'].mean()
    st.markdown("**Average Waste (kg/day)**")
    st.markdown(f"### {avg_waste:.2f}")
    st.markdown("kg per capita per day")

with col2:
    highest_country = df.loc[df['msw_kg_per_capita_per_day'].idxmax(), 'country_name']
    highest_val = df['msw_kg_per_capita_per_day'].max()
    st.markdown("**Highest Waste Country**")
    st.markdown(f"### {highest_country}")
    st.markdown(f"🔺 {highest_val:.2f} kg/day")

with col3:
    lowest_country = df.loc[df['msw_kg_per_capita_per_day'].idxmin(), 'country_name']
    lowest_val = df['msw_kg_per_capita_per_day'].min()
    st.markdown("**Lowest Waste Country**")
    st.markdown(f"### {lowest_country}")
    st.markdown(f"🔻 {lowest_val:.2f} kg/day")

with col4:
    total_waste = df['msw_tonnes_per_year'].sum()
    st.markdown("**Total Waste Generated**")
    st.markdown(f"#### {total_waste:,.0f}")
    st.markdown("tonnes per year")

# Income chart
income_avg = df.groupby('income_group')['msw_kg_per_capita_per_day'].mean().reset_index()
fig = px.pie(income_avg, values='msw_kg_per_capita_per_day',
             names='income_group',
             hole=0.5,
             title='Waste by Income Group')
st.plotly_chart(fig)

# Region chart
region_avg = df.groupby('region')['msw_kg_per_capita_per_day'].mean().reset_index()
fig = px.bar(region_avg, x='msw_kg_per_capita_per_day', y='region',
             orientation='h', color='region',
             title='Waste per Capita by Region',
             labels={'msw_kg_per_capita_per_day': 'Average Waste (kg/capita/day)',
                     'region': 'Region'})
st.plotly_chart(fig, use_container_width=True)

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

#world map
import plotly.express as px

st.subheader("🌍 Global Waste Map")

# Dropdown 
map_metric = st.selectbox(
    "Select metric to display on the map",
    options=[
        "Total waste generated (t/year)",
        "Waste per capita (kg/capita/day)",
        "Collection coverage (%)"
    ]
)

# Map selection 
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

#tree map

fig = px.treemap(df, path=['region', 'country_name'],
                 values='msw_tonnes_per_year',
                 title='Waste Generation by Region and Country')
st.plotly_chart(fig)

#MSW Tonnes per Year – by Each Year (Bar Chart)
yearly = df.groupby('year_reported')['msw_tonnes_per_year'].sum().reset_index()

fig = px.bar(yearly, x='year_reported', y='msw_tonnes_per_year',
             title='Total Waste Generated Each Year',
             labels={'year_reported': 'Year', 'msw_tonnes_per_year': 'Total Waste (tonnes)'},
             color='msw_tonnes_per_year',
             color_continuous_scale='Reds')
st.plotly_chart(fig)

#bubble chart
fig = px.scatter(df, x='population', y='msw_tonnes_per_year',
                 size='msw_tonnes_per_year',
                 color='region', hover_name='country_name',
                 log_x=True, log_y=True,
                 title='Population vs Waste Generation (bubble size = waste amount)',
                 labels={'population': 'Population (log scale)',
                         'msw_tonnes_per_year': 'Total Waste (tonnes, log scale)'})
st.plotly_chart(fig)

#line chart
# Get the 2 most recent years in your filtered data
recent_years = sorted(df['year_reported'].unique())[-2:]

# Filter for only those 2 years
df_recent = df[df['year_reported'].isin(recent_years)]
region_total = df_recent.groupby(['year_reported', 'region'])['msw_tonnes_per_year'].sum().reset_index()

fig = px.line(region_total,
              x='year_reported',
              y='msw_tonnes_per_year',
              color='region',
              markers=True,
              title='Total Waste Generated by Region (Last 2 Years)',
              labels={'year_reported': 'Year',
                      'msw_tonnes_per_year': 'Total Waste (tonnes)',
                      'region': 'Region'})
st.plotly_chart(fig, use_container_width=True)

#preview
with st.expander("Data Preview"):
    st.dataframe(df)