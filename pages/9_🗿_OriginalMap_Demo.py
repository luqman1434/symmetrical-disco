import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import math
from shapely.geometry import Point
from streamlit_folium import st_folium

# Initialization of Streamlit's session state variable
if 'sidebar_data' not in st.session_state:
    st.session_state.sidebar_data = ''

def read_file(filename, sheetname):
    """Function to read the Excel file."""
    excel_file = pd.ExcelFile(filename)
    data_d = excel_file.parse(sheet_name=sheetname)
    return data_d

def plot_markers(map_obj, data):
    """Function to plot markers on the map."""
    for itp_data in data.to_dict(orient='records'):
        latitude = itp_data['map_latitude']
        longitude = itp_data['map_longitude']
        company_name = itp_data['Company name']
        data_str = company_name + ': ' + itp_data['Company address']
        popup_content = f"""
        <div>
            {company_name}<br>
            <a href="/?sidebar_data={data_str}">Show in sidebar</a>
        </div>
        """
        if not math.isnan(latitude) and not math.isnan(longitude):
            folium.Marker(location=[latitude, longitude], popup=popup_content, tooltip=company_name).add_to(map_obj)

st.title('Available ITP companies in Malaysia')

file_input = 'MMU ITP List 13_9_9_11.xlsx'
geojson_file = "msia_district.geojson"

# Reading geojson and data
with open(geojson_file, encoding='utf-8', errors='ignore') as gj_f:
    geojson_data = gpd.read_file(gj_f)
itp_list_state = read_file(file_input, 0)

map_my = folium.Map(location=[4.2105, 108.9758], zoom_start=6)

itp_list_state['geometry'] = itp_list_state.apply(lambda x: Point(x['map_longitude'], x['map_latitude']), axis=1)
itp_list_state = gpd.GeoDataFrame(itp_list_state, geometry='geometry')

selected_states = st.multiselect('Select States', itp_list_state['STATE'].unique())
filtered_data = itp_list_state[itp_list_state['STATE'].isin(selected_states)]

# Plot markers on the map
plot_markers(map_my, filtered_data)

show_choropleth = st.checkbox("Show Choropleth", value=False)
if show_choropleth:
    plot_choropleth(map_my) # Assuming this function remains the same as in your initial code

st_folium(map_my)

# Display sidebar data
if st.session_state.sidebar_data:
    st.sidebar.text(st.session_state.sidebar_data)

# Update sidebar data if received from the map
sidebar_data = st.experimental_get_query_params().get('sidebar_data')
if sidebar_data:
    st.session_state.sidebar_data = sidebar_data[0]
