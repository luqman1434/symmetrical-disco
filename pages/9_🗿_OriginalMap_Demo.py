# app.py
import streamlit as st
import pandas as pd

# Load the dataset
@st.cache
def load_data():
    # Assuming the Excel file is named "companies.xlsx" and the sheet name is "Sheet1"
    data = pd.read_excel("companies.xlsx", engine="openpyxl")
    return data

df = load_data()

# Streamlit App UI
st.title('Company Search App')

# Text Input for Company Name Search
search_term = st.text_input("Enter Company Name:")

if search_term:
    # Filter dataframe based on user input
    results = df[df['Company'].str.contains(search_term, case=False, na=False)]

    # Display results
    st.write(results)

# Run this by typing 'streamlit run app.py' in the terminal

