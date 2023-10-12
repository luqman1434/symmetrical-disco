# app.py
import streamlit as st
import pandas as pd
from html import escape

# Load the dataset
@st.cache
def load_data():
    # Use the specified Excel file name
    data = pd.read_excel("MMU ITP List 13_9_9_11.xlsx", engine="openpyxl")
    return data

df = load_data()

# Streamlit App UI
st.title('Company Search App')

# Custom styles to expand table width
st.markdown("""
<style>
.dataframe {
    white-space: nowrap;
    width: 100%;
    overflow: scroll;
}
</style>
""", unsafe_allow_html=True)

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

# Define columns to display
columns_to_display = ["Company name", "Company address", "website_url", "Company Tel", "Company Email"]

# Filter by search term and selected states
if search_term:
    filtered_df = df[df['Company name'].str.contains(search_term, case=False, na=False)]
else:
    filtered_df = df

filtered_df = filtered_df[filtered_df['STATE'].isin(selected_states)]

# Define a function to create an HTML card for each company
def create_card(row):
    # Ensure data is a string or replace with an empty string
    company_name = escape(str(row['Company name'])) if not pd.isna(row['Company name']) else ""
    company_address = escape(str(row['Company address'])) if not pd.isna(row['Company address']) else ""
    website_url = f"<a href='{escape(str(row['website_url']))}' target='_blank'>{escape(str(row['website_url']))}</a>" if not pd.isna(row['website_url']) else ""
    company_tel = escape(str(row['Company Tel'])) if not pd.isna(row['Company Tel']) else ""
    company_email = escape(str(row['Company Email'])) if not pd.isna(row['Company Email']) else ""

    card = f"""
    <div style="border:1px solid #eee; border-radius:5px; padding:10px; margin:5px; width: 30%; height: 300px; overflow: auto; display:inline-block; vertical-align:top">
        <h4>{company_name}</h4>
        <p>{company_address}</p>
        <p>{website_url}</p>
        <p>{company_tel}</p>
        <p>{company_email}</p>
    </div>
    """
    return card



# Convert the filtered DataFrame to HTML cards
cards = filtered_df[columns_to_display].apply(create_card, axis=1).tolist()

for i in range(0, len(cards), 3):
    row_cards = ''.join(cards[i:i+3])
    st.markdown(row_cards, unsafe_allow_html=True)

# Run this by typing 'streamlit run app.py' in the terminal
