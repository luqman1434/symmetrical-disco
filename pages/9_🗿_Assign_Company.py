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

# Text input for partial specialization search
spec_input = st.text_input("Enter Specialization (Partial Match):")

# User input for X value
X = st.number_input("Enter X value:")
min_dist = X / 111

nearest_company = []

if not spec_input:
    spec_input = ''  # If no input provided, consider all specializations

for index, company in itp_df.iterrows():
    company_specializations = company['Specialization'].split(', ')
    exact_match_found = False

    for spec in company_specializations:
        if spec_input == spec:
            exact_match_found = True
            break

    if not exact_match_found:
        for spec in company_specializations:
            if spec_input in spec:
                xy1 = [latitude, longitude]
                xy2 = [company['map_latitude'], company['map_longitude']]
                distance = math.dist(xy1, xy2)
                if distance <= min_dist:
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
