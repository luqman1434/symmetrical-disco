import math
import pandas as pd
import streamlit as st

# Load the Excel file
itp_file = pd.ExcelFile('FACULTY_ASSIGNED_SPEC.xlsx')
itp_df = itp_file.parse(sheet_name=0)

# Streamlit UI
st.title('Find Nearest Companies')

# User input for coordinates
st.sidebar.header('Input Coordinates')
x = st.sidebar.number_input('X Coordinate:', min_value=-90.0, max_value=90.0, step=0.0001, format='%.7f')
y = st.sidebar.number_input('Y Coordinate:', min_value=-180.0, max_value=180.0, step=0.0001, format='%.7f')

# User input for minimum distance
min_dist = st.sidebar.number_input('Minimum Distance (in degrees):', value=3.0)

# Filter companies based on specialization
spec = "'EB01'"
selected_company = itp_df.loc[itp_df['Specialization'] == spec]

# Calculate distances and filter nearby companies
nearest_company = []
for index, company in selected_company.iterrows():
    xy1 = [x, y]
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

# Display the nearest companies in a DataFrame
nearest_company_df = pd.DataFrame(nearest_company)
st.write(nearest_company_df)

# Save the DataFrame to an Excel file
if st.button('Save Nearest Companies'):
    nearest_company_df.to_excel('nearest.xlsx', index=False)
    st.success('Nearest companies saved to nearest.xlsx')
