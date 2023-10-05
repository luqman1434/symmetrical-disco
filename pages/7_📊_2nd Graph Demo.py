import streamlit as st
import pandas as pd
import plotly.express as px

# Load data from the 'ngee.csv' file (replace with your actual file path if needed)
data = pd.read_csv('MMU ITP List.csv')

# Streamlit app
st.title("Pie Chart Filter")

# Sidebar
state_filter = st.sidebar.selectbox("Filter by State", data['STATE'].unique())

# Filter data based on state selection
filtered_data = data if state_filter == 'All' else data[data['STATE'] == state_filter]

# Display overall state pie chart
st.subheader("Overall State Distribution")
state_counts = data['STATE'].value_counts()  # Count all states, not just filtered ones
state_pie_fig = px.pie(names=state_counts.index, values=state_counts.values)
st.plotly_chart(state_pie_fig)

# Filter by city within the selected state
if state_filter != 'All':
    city_filter = st.sidebar.selectbox("Filter by City", data[data['STATE'] == state_filter]['CITY'].unique())
    st.subheader(f"City Distribution in {state_filter}")
    
    # Count all cities for the selected state from the original dataset
    city_counts = data[data['STATE'] == state_filter]['CITY'].value_counts()
    city_pie_fig = px.pie(names=city_counts.index, values=city_counts.values)
    st.plotly_chart(city_pie_fig)

    # Filter by address within the selected city
    if city_filter != 'All':
        st.subheader(f"Address Distribution in {city_filter}")
        address_counts = data[(data['STATE'] == state_filter) & (data['CITY'] == city_filter)]['ADDRESS'].value_counts()
        address_pie_fig = px.pie(names=address_counts.index, values=address_counts.values)
        st.plotly_chart(address_pie_fig)
