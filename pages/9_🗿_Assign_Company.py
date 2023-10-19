!pip install geopy

import streamlit as st
import math
import pandas as pd
from geopy.geocoders import Nominatim

# Load the Excel file
itp_file = pd.ExcelFile('FACULTY_ASSIGNED_SPECIALIZATION.xlsx')
itp_df = itp_file.parse(sheet_name=0)

st.title("Nearest Companies Finder")

# Sidebar section for geocoding
st.sidebar.title("Geocode Location")
location = st.sidebar.text_input("Enter a location/address for geocoding:")

geocoder = Nominatim(user_agent="geocoding_app")

if location:
    location_data = geocoder.geocode(location)
    if location_data:
        st.sidebar.write("Location Details:")
        st.sidebar.write(f"Address: {location_data.address}")
        st.sidebar.write(f"Latitude: {location_data.latitude}")
        st.sidebar.write(f"Longitude: {location_data.longitude}")

        # User input for coordinates with more decimal places
        latitude = location_data.latitude
        longitude = location_data.longitude

# Main content for nearest companies
spec = "'EB01'"

# User input for X value
X = st.number_input("Enter X value:")
min_dist = X / 111

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
