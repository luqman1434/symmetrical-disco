import streamlit as st
import math
import pandas as pd

# Load the Excel file
itp_file = pd.ExcelFile('FACULTY_ASSIGNED_SPECIALIZATION.xlsx')
itp_df = itp_file.parse(sheet_name=0)

st.title("Nearest Companies Finder")

# User input for coordinates with more decimal places
latitude = st.number_input("Enter Latitude:", format="%.6f")
longitude = st.number_input("Enter Longitude:", format="%.6f")

# Text input for specialization (partial match)
spec_input = st.text_input("Enter Specialization (Partial Match):")

# User input for X value
X = st.number_input("Enter X value:")
min_dist = X / 111

nearest_company = []

if spec_input:
    # Filter the DataFrame for rows where 'Specialization' contains the user input
    selected_company = itp_df[itp_df['Specialization'].str.contains(spec_input)]
else:
    # If no input provided, consider all companies
    selected_company = itp_df

for index, company in selected_company.iterrows():
    xy1 = [latitude, longitude]
    xy2 = [company['map_latitude'], company['map_longitude']]
    distance = math.dist(xy1, xy2)
    if distance <= min_dist:
        temp_dict = {
            'Company name': company['Company name'],
            'Company address': company['Company address'],
            'Distance from location (km)': distance * 111,
            'Specialization': company['Specialization']
        }
        nearest_company.append(temp_dict)

if nearest_company:
    nearest_company_df = pd.DataFrame(nearest_company)
    st.dataframe(nearest_company_df)
else:
    st.write("No matching companies found within the specified distance.")
