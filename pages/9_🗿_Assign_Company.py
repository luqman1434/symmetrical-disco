import streamlit as st
import math
import pandas as pd

# Load the Excel file
itp_file = pd.ExcelFile('FACULTY_ASSIGNED_SPECIALIZATION.xlsx')
itp_df = itp_file.parse(sheet_name=0)

st.title("Nearest Companies Finder")

# User input for coordinates
latitude = st.number_input("Enter Latitude:")
longitude = st.number_input("Enter Longitude:")

spec = "'EB01'"
min_dist = 3.0 / 111

nearest_company = []
selected_company = itp_df.loc[itp_df['Specialization'] == spec]
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

# Save the Streamlit app as a .py file and run it with `streamlit run your_app.py`
