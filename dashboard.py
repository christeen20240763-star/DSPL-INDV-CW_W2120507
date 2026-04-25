import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

df = pd.read_excel("/Users/delphina/Downloads/YEAR 02/DSPL/DSPL 2/DSPL CW 2/cleaned_what_a_waste_data.xlsx")

st.markdown("""
    <style>
    .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

# SIDEBAR 
st.sidebar.title("Global Waste Dashboard")
st.sidebar.markdown("---")  

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

st.markdown("**Exploring global waste generation, income levels, regional patterns, and sustainability gaps.**")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---") 


st.markdown("<br>", unsafe_allow_html=True)

def kpi_card(title, value, subtitle, subtitle_color="limegreen"):
    st.markdown(f"""
        <div style="padding:15px 20px; margin:5px;">
            <p style="color:white; 
                      font-size:15px; 
                      font-weight:900; 
                      margin:0;
                      letter-spacing:0.5px;">{title}</p>
            <h2 style="color:white; 
                       margin:8px 0; 
                       font-size:28px;">{value}</h2>
            <div style="margin-top:10px;">
                <span style="background-color:darkgreen; 
                             color:{subtitle_color}; 
                             padding:6px 12px; 
                             border-radius:15px; 
                             font-size:13px;
                             white-space:nowrap;">
                    {subtitle}
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("Average Waste (kg/day)",
             f"{df['msw_kg_per_capita_per_day'].mean():.2f}",
             "kg per capita per day")

with col2:
    highest_country = df.loc[df['msw_kg_per_capita_per_day'].idxmax(), 'country_name']
    kpi_card("Highest Waste Country",
             highest_country,
             f"🔺 {df['msw_kg_per_capita_per_day'].max():.2f} kg/day")

with col3:
    lowest_country = df.loc[df['msw_kg_per_capita_per_day'].idxmin(), 'country_name']
    kpi_card("Lowest Waste Country",
             lowest_country,
             f"🔻 {df['msw_kg_per_capita_per_day'].min():.2f} kg/day",
             subtitle_color="red") 

with col4:
    total_waste = df['msw_tonnes_per_year'].sum()
    kpi_card("Total Waste Generated",
             f"{total_waste:,.0f}",
             "tonnes per year")

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
top10 = df.nlargest(10, 'msw_tonnes_per_year')[['country_name', 'msw_tonnes_per_year']].sort_values('msw_tonnes_per_year')

fig = px.bar(top10,
             x='msw_tonnes_per_year',
             y='country_name',
             orientation='h',
             title='Top 10 Waste Generating Countries',
             labels={'msw_tonnes_per_year': 'Total Waste (tonnes/year)',
                     'country_name': 'Country'},
             color='msw_tonnes_per_year',
             color_continuous_scale='reds',
             text='msw_tonnes_per_year')

fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(height=500, showlegend=False, coloraxis_showscale=False)

st.plotly_chart(fig, use_container_width=True)

# Waste composition
yearly_comp = df.groupby('year_reported')[
    ['composition_food%_weight_msw',
     'composition_paper_cardboard%_weight_msw',
     'composition_plastic%_weight_msw']
].mean().reset_index()

fig = px.bar(yearly_comp,
             x='year_reported',
             y=['composition_food%_weight_msw',
                'composition_paper_cardboard%_weight_msw',
                'composition_plastic%_weight_msw'],
             title='Waste Composition by Year',
             labels={'year_reported': 'Year',
                     'value': 'Proportion',
                     'variable': 'Waste Type'},
             barmode='stack',
             color_discrete_map={
                 'composition_food%_weight_msw': 'steelblue',
                 'composition_paper_cardboard%_weight_msw': 'coral',
                 'composition_plastic%_weight_msw': 'seagreen'
             })
fig.update_xaxes(
    tickmode='array',
    tickvals=yearly_comp['year_reported'].tolist(),
    ticktext=[str(int(y)) for y in yearly_comp['year_reported'].tolist()],
    tickangle=45,  
    tickfont=dict(size=14)) 

fig.update_layout(height=500,legend_title='Waste Type') 

                  
st.plotly_chart(fig, use_container_width=True)

#world map
import plotly.express as px

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

map_df = df[["country_name", map_column]].dropna()

fig_map = px.choropleth(
    map_df,
    locations="country_name",
    locationmode="country names",
    color=map_column,
    hover_name="country_name",
    title=f"Global Map of {map_metric}",
    
    color_continuous_scale="Plasma"
)

fig_map.update_layout(
    margin=dict(l=0, r=0, t=50, b=0)
)

st.plotly_chart(fig_map, use_container_width=True)



#MSW Tonnes per Year by Each Year (Bar Chart)

yearly = df.groupby('year_reported')['msw_tonnes_per_year'].sum().reset_index()

fig = px.bar(yearly, 
             x='year_reported', 
             y='msw_tonnes_per_year',
             title='Total Waste Generated Each Year',
             labels={'year_reported': 'Year', 
                     'msw_tonnes_per_year': 'Total Waste (tonnes)'},
             color='msw_tonnes_per_year',
             color_continuous_scale='Reds')
fig.update_xaxes(
    tickmode='array',
    tickvals=yearly['year_reported'].tolist(),
    ticktext=[str(int(y)) for y in yearly['year_reported'].tolist()]
)

st.plotly_chart(fig, use_container_width=True)

#line chart waste per capita over time by region
yearly = df.groupby('year_reported')['msw_tonnes_per_year'].sum().reset_index()

fig = px.line(yearly,
              x='year_reported',
              y='msw_tonnes_per_year',
              title='Trend of Waste Generation Over Years',
              markers=True,
              labels={'year_reported': 'Year',
                      'msw_tonnes_per_year': 'Total Waste (tonnes)'})

fig.update_xaxes(
    tickmode='array',
    tickvals=yearly['year_reported'].tolist(),
    ticktext=[str(int(y)) for y in yearly['year_reported'].tolist()])

fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)

#bubble chart
fig = px.scatter(df,
                 x='population',
                 y='msw_tonnes_per_year',
                 size='msw_tonnes_per_year',
                 color='region',
                 hover_name='country_name',
                 log_x=True,
                 log_y=True,
                 size_max=60,
                 title='Population vs Waste Generation (bubble size = waste amount)',
                 labels={'population': 'Population (log scale)',
                         'msw_tonnes_per_year': 'Total Waste (tonnes, log scale)',
                         'region': 'Region'})

fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)

#line chart msw tonnes per year 2 most recent years 
recent_years = sorted(df['year_reported'].unique())[-2:]

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