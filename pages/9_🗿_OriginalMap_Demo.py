# app.py
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

# Text Input for Company Name Search in the sidebar
search_term = st.sidebar.text_input("Enter Company Name:")

# Generate checkboxes for each state in the sidebar
unique_states = sorted(df['STATE'].dropna().unique())
selected_states = [state for state in unique_states if st.sidebar.checkbox(state, True)]

# Define columns to display
columns_to_display = ["Company name", "Company address", "website_url", "Company Tel", "Company Email"]

# Filter by search term and selected states
# Filter by search term and selected states
if search_term:
    filtered_df = df[df['Company name'].str.contains(search_term, case=False, na=False)]
else:
    filtered_df = df

filtered_df = filtered_df[filtered_df['STATE'].isin(selected_states)]

# Display the filtered data
st.write(filtered_df[columns_to_display])

# Run this by typing 'streamlit run app.py' in the terminal
