import streamlit as st
import math
import pandas as pd

# Load the Excel file
itp_file = pd.ExcelFile('FACULTY_ASSIGNED_SPECIALIZATION.xlsx')
itp_df = itp_file.parse(sheet_name=0)

# Remove single quotes from the 'Specialization' column
itp_df['Specialization'] = itp_df['Specialization'].astype(str).str.replace("'", "")

st.title("Nearest Companies Finder")

# User input for coordinates with more decimal places
latitude = st.number_input("Enter Latitude:", format="%.6f")
longitude = st.number_input("Enter Longitude:", format="%.6f")

# Multiselect input for specialization search
spec_inputs = st.multiselect(
    "Select Specializations:",
    options=['EB01', 'EB02', 'EB03', 'EB04', 'DD09', 'DD14', 'EF01', 'KB04', 'KFO01', 'EB10']
)

# User input for X value
X = st.number_input("Enter X value:")
min_dist = X / 111

nearest_company = []

for index, company in itp_df.iterrows():
    company_specializations = company['Specialization'].split(', ')
    matching_specs = [spec for spec in company_specializations if any(input_spec in spec for input_spec in spec_inputs)]
    if matching_specs:  # Only proceed if there are any matching specializations
        xy1 = [latitude, longitude]
        xy2 = [company['map_latitude'], company['map_longitude']]
        distance = math.dist(xy1, xy2)
        if distance <= min_dist:
            for spec in matching_specs:  # Loop through all matching specializations
                temp_dict = {
                    'Company name': company['Company name'],
                    'Company address': company['Company address'],
                    'Distance from location (km)': distance * 111,
                    'Specialization': spec
                }
                nearest_company.append(temp_dict)

if nearest_company:
    nearest_company_df = pd.DataFrame(nearest_company)
    st.dataframe(nearest_company_df)
else:
    st.write("No matching companies found within the specified distance.")
