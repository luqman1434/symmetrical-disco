import streamlit as st
import pandas as pd
import geopandas as gpd
# import os
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")

st.set_page_config(page_title="Graphing Dataset Demo", page_icon="📊") #📊_GraphingDataset_Demo.py
st.markdown("# Graphing Demo")
##
st.sidebar.header("Graphing Demo")
st.write(
    """This part of the website shows a general overview of the data in terms of how much companies are in each state, broken down into district. This can show in what states and districts are the companies most 
    grouped in, inside Malaysia"""
)
##


import streamlit as st
import pandas as pd
import plotly.express as px

# Load data from the 'ngee.csv' file (replace with your actual file path if needed)
# data = pd.read_csv('MMU ITP List.csv')
# Specify the file name
file_name = "MMU ITP List 13_9_9_11.xlsx"

try:
    df = pd.read_excel(file_name, engine='openpyxl')
except FileNotFoundError:
    st.error(f"File '{file_name}' not found.")



# Streamlit app
st.title("Pie Chart Filter")

# Sidebar
# state_filter = st.sidebar.selectbox("Filter by State", data['STATE'].unique())
state_filter = st.sidebar.selectbox("Filter by State", df['STATE'].unique())


# Filter data based on state selection
# filtered_data = data if state_filter == 'All' else data[data['STATE'] == state_filter]
filtered_data = df if state_filter == 'All' else df[df['STATE'] == state_filter]


# Display overall state pie chart
st.subheader("Overall State Distribution")
# state_counts = data['STATE'].value_counts()  # Count all states, not just filtered ones
state_counts = df['STATE'].value_counts()  # Count all states, not just filtered ones
state_pie_fig = px.pie(names=state_counts.index, values=state_counts.values)
st.plotly_chart(state_pie_fig)

# Filter by city within the selected state
if state_filter != 'All':
    # city_filter = st.sidebar.selectbox("Filter by City", data[data['STATE'] == state_filter]['CITY'].unique())
    city_filter = st.sidebar.selectbox("Filter by City", df[df['STATE'] == state_filter]['CITY'].unique())
    st.subheader(f"City Distribution in {state_filter}")
    
    # Count all cities for the selected state from the original dataset
    # city_counts = data[data['STATE'] == state_filter]['CITY'].value_counts()
    city_counts = df[df['STATE'] == state_filter]['CITY'].value_counts()
    city_pie_fig = px.pie(names=city_counts.index, values=city_counts.values)
    st.plotly_chart(city_pie_fig)

    # Filter by address within the selected city
    if city_filter != 'All':
        st.subheader(f"Address Distribution in {city_filter}")
        # address_counts = data[(data['STATE'] == state_filter) & (data['CITY'] == city_filter)]['ADDRESS'].value_counts()
        address_counts = df[(df['STATE'] == state_filter) & (df['CITY'] == city_filter)]['ADDRESS'].value_counts()
        address_pie_fig = px.pie(names=address_counts.index, values=address_counts.values)
        st.plotly_chart(address_pie_fig)
