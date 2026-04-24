import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Global Waste Dashboard")

df = pd.read_excel("/Users/delphina/Downloads/YEAR 02/DSPL/DSPL 2/DSPL CW 2/cleaned_what_a_waste_data.xlsx")

#KPI
st.header("Key Insights")

col1, col2, col3 = st.columns(3)

# Metrics
avg_waste = df['msw_kg_per_capita_per_day'].mean()
top = df.loc[df['msw_kg_per_capita_per_day'].idxmax()]
low = df.loc[df['msw_kg_per_capita_per_day'].idxmin()]

col1.metric("Average Waste (kg/day)", round(avg_waste, 2))

col2.markdown("**Highest Waste Country**")
col2.write(f"{top['country_name']} ({round(top['msw_kg_per_capita_per_day'],2)} kg/day)")

col3.markdown("**Lowest Waste Country**")
col3.write(f"{low['country_name']} ({round(low['msw_kg_per_capita_per_day'],2)} kg/day)")
