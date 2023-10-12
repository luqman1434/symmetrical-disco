import streamlit as st
import pandas as pd

# Load the dataset
@st.cache
def load_data():
    # Use the specified Excel file name
    data = pd.read_excel("MMU ITP List 13_9_9_11.xlsx", engine="openpyxl")
    return data

df = load_data()

# Streamlit App UI
st.title('Company Search App')

# Title for the filters in the sidebar
st.sidebar.header('Filter by State')

# Generate checkboxes for each state in the sidebar
unique_states = sorted(df['STATE'].dropna().unique())

# Add a "Select All" checkbox in the sidebar
select_all = st.sidebar.checkbox("Select All", True)

if select_all:
    selected_states = unique_states
    for state in unique_states:
        st.sidebar.checkbox(state, value=True, key=state)
else:
    selected_states = [state for state in unique_states if st.sidebar.checkbox(state, False, key=state)]

# Text Input for Company Name Search above the table
search_term = st.text_input("Enter Company Name:")

# Filter by search term and selected states
if search_term:
    filtered_df = df[df['Company name'].str.contains(search_term, case=False, na=False)]
else:
    filtered_df = df

filtered_df = filtered_df[filtered_df['STATE'].isin(selected_states)]

def display_card(row):
    # Start a container for the card
    with st.container():
        
        # Create three columns (or adjust based on your layout needs)
        col1, col2, col3 = st.columns([1,1,1])
        
        with col1:
            if not pd.isna(row['Company name']):
                st.markdown(f"**{row['Company name']}**")
            if not pd.isna(row['Company address']):
                st.write(row['Company address'])
            
        with col2:
            if not pd.isna(row['website_url']):
                st.markdown(f"[{row['website_url']}]({row['website_url']})")
        
        with col3:
            if not pd.isna(row['Company Tel']):
                st.write(row['Company Tel'])
            if not pd.isna(row['Company Email']):
                st.write(row['Company Email'])

for _, row in filtered_df.iterrows():
    display_card(row)
