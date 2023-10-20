import streamlit as st
import pandas as pd
import math
from html import escape
from geopy.geocoders import Nominatim

def create_card(row):
    company_name = escape(str(row['Company name'])) if not pd.isna(row['Company name']) else ""
    company_address = escape(str(row['Company address'])) if not pd.isna(row['Company address']) else ""
    distance = f"{row['Distance from location (km)']:.2f} km" if not pd.isna(row['Distance from location (km)']) else ""
    specialization = escape(str(row['Specialization'])) if not pd.isna(row['Specialization']) else ""
    
    card = f"""
    <div style="border:1px solid #eee; border-radius:5px; padding:10px; margin:5px; width: 30%; height: 300px; overflow: auto; display:inline-block; vertical-align:top">
        <h4>{company_name}</h4>
        <p>{company_address}</p>
        <p>Distance: {distance}</p>
        <p>Specialization: {specialization}</p>
    </div>
    """
    return card

itp_file = pd.ExcelFile('FACULTY_ASSIGNED_SPECIALIZATION.xlsx')
itp_df = itp_file.parse(sheet_name=0)

itp_df['Specialization'] = itp_df['Specialization'].astype(str).str.replace("'", "")

st.title("Nearest Companies Finder")

col1, col2 = st.columns(2)

latitude = col1.number_input("Enter Latitude:", format="%.6f")
longitude = col2.number_input("Enter Longitude:", format="%.6f")

spec_inputs = st.multiselect(
    "Select Specializations:",
    options=['EB01', 'EB02', 'EB03', 'EB04', 'DD09', 'DD14', 'EF01', 'KB04', 'KFO01', 'EB10', 'NONE']
)

# User input for X value
X = st.number_input("Enter maximum distance to display the companies:")
min_dist = X / 111

nearest_company = []

for index, company in itp_df.iterrows():
    company_specializations = company['Specialization'].split(', ')
    matching_specs = [spec for spec in company_specializations if any(input_spec in spec for input_spec in spec_inputs)]
    if 'NONE' in spec_inputs and company['Specialization'] == '':
        matching_specs.append('NONE')
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
    
    sort_by_distance = st.checkbox('Sort by Distance')
    sort_by_name = st.checkbox('Sort by Name')
    
    if sort_by_distance:
        nearest_company_df = nearest_company_df.sort_values(by='Distance from location (km)')
    elif sort_by_name:
        nearest_company_df = nearest_company_df.sort_values(by='Company name')
    
    # Convert the DataFrame to HTML cards
    cards = nearest_company_df.apply(create_card, axis=1).tolist()
    cards_html = ''.join(cards)
    st.markdown(cards_html, unsafe_allow_html=True)
else:
    st.write("No matching companies found within the specified distance.")

# Function to geocode a location
def geocode_location(location):
    geolocator = Nominatim(user_agent="geocoding_app")
    location = geolocator.geocode(location)
    if location:
        return location.latitude, location.longitude
    return None, None

# Sidebar for geocoding
st.sidebar.title("Geocoding")
location_input = st.sidebar.text_input("Enter Location:")
if location_input:
    latitude, longitude = geocode_location(location_input)
    if latitude and longitude:
        st.sidebar.write(f"Latitude: {latitude}")
        st.sidebar.write(f"Longitude: {longitude}")
    else:
        st.sidebar.write("Location not found.")
