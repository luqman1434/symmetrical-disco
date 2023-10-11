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

# Text Input for Company Name Search
search_term = st.text_input("Enter Company Name:")

# Define columns to display
columns_to_display = ["Company name", "Company address", "website_url", "Company Tel", "Company Email"]

if search_term:
    # Filter dataframe based on user input
    results = df[df['Company name'].str.contains(search_term, case=False, na=False)]
else:
    # If no search term is entered, display all the companies
    results = df

# Display only the specified columns from the results
st.write(results[columns_to_display])

# Run this by typing 'streamlit run app.py' in the terminal
