import streamlit as st
import pandas as pd
from html import escape

# Load the dataset
@st.cache
def load_data():
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

# Define a function to create an HTML card for each company
# ...

# Define a function to create an HTML card for each company
# Define a function to create an HTML card for each company
def create_card(row):
    company_name_data = str(row['Company name']).strip("'")
    company_name = f"<h4>{company_name_data}</h4>" if not pd.isna(row['Company name']) else ""

    company_address_data = str(row['Company address']).strip("'")
    company_address = f"<p>{company_address_data}</p>" if not pd.isna(row['Company address']) else ""

    website_url_data = str(row['website_url']).strip("'")
    website_url = f"<p><a href='{website_url_data}' target='_blank'>{website_url_data}</a></p>" if not pd.isna(row['website_url']) else ""

    # Ensure the phone number has only digits or hyphens
    company_tel_data = ''.join([c for c in str(row['Company Tel']) if c.isdigit() or c == '-'])
    company_tel = f"<p>{company_tel_data}</p>" if not pd.isna(row['Company Tel']) else ""

    # Strip single quotes around emails
    company_email_data = str(row['Company Email']).strip("'")
    company_email = f"<p>{company_email_data}</p>" if not pd.isna(row['Company Email']) else ""

    card = f"""
    <div style="border:1px solid #eee; border-radius:5px; padding:10px; margin:5px; width: 30%; height: 300px; overflow: auto; display:inline-block; vertical-align:top">
        {company_name}
        {company_address}
        {website_url}
        {company_tel}
        {company_email}
    </div>
    """
    return card


# ...


# Convert the filtered DataFrame to HTML cards
cards = filtered_df.apply(create_card, axis=1).tolist()

for i in range(0, len(cards), 3):
    row_cards = ''.join(cards[i:i+3])
    st.markdown(row_cards, unsafe_allow_html=True)

# Run this by typing 'streamlit run app.py' in the terminal
