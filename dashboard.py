import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

col4, col5 = st.columns(2)

# Income vs Waste
with col4:
    st.subheader("Higher income countries generate more waste per capita")
    fig, ax = plt.subplots()
    df.groupby('income_group')['msw_kg_per_capita_per_day'].mean().plot(kind='bar', ax=ax, color=['red', 'orange', 'green', 'blue'])
    ax.set_ylabel("kg per capita per day")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Region vs Waste
import numpy as np
import matplotlib.pyplot as plt

with col5:
    st.subheader("Waste per capita varies across regions")

    data = df.groupby('region')['msw_kg_per_capita_per_day'].mean().sort_values()

    fig, ax = plt.subplots()

    # 🌱 Create gradient colors (light → dark green)
    colors = plt.cm.Greens(np.linspace(0.3, 0.9, len(data)))

    ax.bar(data.index, data.values, color=colors)
    ax.set_ylabel("kg per capita per day")
    plt.xticks(rotation=45)

    st.pyplot(fig)

    #top 10 waste countries
    

st.subheader("Top 10 Waste Generating Countries")

top10 = df.nlargest(10, 'msw_tonnes_per_year')

fig, ax = plt.subplots()


colors = plt.cm.Reds(np.linspace(0.9, 0.3, len(top10)))

ax.bar(top10['country_name'], top10['msw_tonnes_per_year'], color=colors)

plt.xticks(rotation=45)
ax.set_ylabel("Total Waste (tonnes/year)")

st.pyplot(fig)

st.subheader("Waste Composition")

labels = ['Food', 'Paper', 'Plastic']
values = [
    df['composition_food%_weight_msw'].mean(),
    df['composition_paper_cardboard%_weight_msw'].mean(),
    df['composition_plastic%_weight_msw'].mean()
]

fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct='%1.1f%%')
st.pyplot(fig)