import streamlit as st
import pandas as pd
import geopandas as gpd
import warnings
import math
import json
import folium
from branca.element import Figure
from shapely.geometry import Point
import streamlit.components.v1 as components

st.set_page_config(page_title="2nd Graph Choropleth Demo", page_icon="🗺")
st.markdown("# 2nd Graph Choropleth Demo")

st.sidebar.header("2nd Graph Choropleth Demo Demo")
st.write(
    """This version of the map shows how the map works with two different filters. One of the filters toggle the choropleth mask on/off on the filter. Another one of the filters toggle on the activation of the 
    pushpins so we can focus on specific filters inside the map."""
)

def read_file(filename, sheetname):
    excel_file = pd.ExcelFile(filename)
    data_d = excel_file.parse(sheet_name=sheetname)
    return data_d

def plot_choropleth(map_obj, show_choropleth=True):
    if show_choropleth:
        choropleth = folium.Choropleth(
            geo_data=merged_gdf,
            name='choropleth',
            data=merged_gdf,
            columns=['NAME_2', 'count'],
            key_on='feature.properties.NAME_2',
            fill_color='RdYlGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            threshold_scale=threshold_scale,
            line_color='black',
            legend_name='District Counts',
            highlight=False
        ).add_to(map_obj)
        folium.GeoJsonTooltip(fields=['NAME_1','NAME_2', 'count'], aliases=['State','District', 'Count']).add_to(choropleth.geojson)

file_input = 'MMU ITP List 13_9_9_11.xlsx'
geojson_file = "msia_district.geojson"

with open(geojson_file, encoding='utf-8', errors='ignore') as gj_f:
    geojson_data = gpd.read_file(gj_f)

itp_list_state = read_file(file_input, 0)
map_size = Figure(width=800, height=600)
map_my = folium.Map(location=[4.2105, 108.9758], zoom_start=6)
map_size.add_child(map_my)

itp_list_state['geometry'] = itp_list_state.apply(lambda x: Point(x['map_longitude'], x['map_latitude']), axis=1)
itp_list_state = gpd.GeoDataFrame(itp_list_state, geometry='geometry')

selected_states = st.multiselect('Select States', itp_list_state['STATE'].unique())
filtered_data = itp_list_state[itp_list_state['STATE'].isin(selected_states)]
joined_data = gpd.sjoin(geojson_data, filtered_data, op="contains").groupby(["NAME_1", "NAME_2"]).size().reset_index(name="count")

merged_gdf = geojson_data.merge(joined_data, on=["NAME_1", "NAME_2"], how="left")
merged_gdf['count'].fillna(0, inplace=True)
threshold_scale = [0, 1, 2, 4, 8, 16, 32, 64, 128, 200, 300, 400]

for itp_data in filtered_data.to_dict(orient='records'):
    latitude = itp_data['map_latitude']
    longitude = itp_data['map_longitude']
    company_name = itp_data['Company name']
    company_address = itp_data['Company address']
    popup_name = '<strong>' + str(company_name) + '</strong>\n' + str(company_address)
    
    # Embed the data in the HTML, which the user can click to "copy"
    embedded_data = '<div data-name="' + company_name + '" data-address="' + company_address + '" onclick="window.clickedCompany=this;">' + popup_name + '</div>'
    popup = folium.Popup(embedded_data, max_width=300)
    marker = folium.Marker(location=[latitude, longitude], tooltip=company_name, popup=popup)
    marker.add_to(map_my)

show_choropleth = st.checkbox("Show Choropleth", value=False)
if show_choropleth:
    plot_choropleth(map_my)

map_my.save('itp_area_map.html')
p = open('itp_area_map.html')
components.html(p.read(), 800, 480)

# JavaScript to get the clicked company data and set the session state
js_code = """
<script>
window.clickedCompany = null;
function saveClickedCompany(){
    if(window.clickedCompany){
        const name = window.clickedCompany.getAttribute('data-name');
        const address = window.clickedCompany.getAttribute('data-address');
        window.Streamlit.setSessionState({'selected_company': {'name': name, 'address': address}});
    }
}
</script>
"""
components.html(js_code, height=0)

# Using session state to show the company details
if "selected_company" not in st.session_state:
    st.session_state.selected_company = {"name": "", "address": ""}

if st.sidebar.button("Show Clicked Company Details"):
    company_name = st.session_state.selected_company["name"]
    company_address = st.session_state.selected_company["address"]
    st.sidebar.markdown("### Company Details")
    st.sidebar.text("Name: " + company_name)
    st.sidebar.text("Address: " + company_address)
