import streamlit as st
import pandas as pd
import geopandas as gpd
import os
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")

st.set_page_config(page_title="2nd Graph Choropleth Demo", page_icon="🗺")
st.markdown("# 2nd Graph Choropleth Demo")

st.sidebar.header("2nd Graph Choropleth Demo Demo")
st.write(
    """This version of the map shows how the map works with two different filters. One of the filters toggle the choropleth mask on/off on the filter. Another one of the filters toggle on the activation of the 
    pushpins so we can focus on specific filters inside the map."""
)

import math
import json
import warnings

import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point

# Define the function to read the Excel file
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

if __name__ == '__main__':
    st.title('Available ITP companies in Malaysia')

    file_input = 'MMU ITP List 13_9_9_11.xlsx'
    geojson_file = "msia_district.geojson"

    text_load_state = st.text('Reading files ...')
    with open(geojson_file, encoding='utf-8', errors='ignore') as gj_f:
        geojson_data = gpd.read_file(gj_f)

    itp_list_state = read_file(file_input, 0)
    text_load_state.text('Reading files ... Done!') 

    map_size = folium.Map(location=[4.2105, 108.9758], zoom_start=6)

    itp_list_state['geometry'] = itp_list_state.apply(lambda x: Point(x['map_longitude'], x['map_latitude']), axis=1)
    itp_list_state = gpd.GeoDataFrame(itp_list_state, geometry='geometry')

    selected_states = st.multiselect('Select States', itp_list_state['STATE'].unique())
    
    filtered_data = itp_list_state[itp_list_state['STATE'].isin(selected_states)]

    joined_data = gpd.sjoin(geojson_data, filtered_data, op="contains").groupby(["NAME_1", "NAME_2"]).size().reset_index(name="count")

    merged_gdf = geojson_data.merge(joined_data, on=["NAME_1", "NAME_2"], how="left")
    merged_gdf['count'].fillna(0, inplace=True)

    threshold_scale = [0, 1, 2, 4, 8, 16, 32, 64, 128, 200, 300, 400] 

    text_load_state.text('Plotting ...')
    for itp_data in filtered_data.to_dict(orient='records'):
        latitude = itp_data['map_latitude']
        longitude = itp_data['map_longitude']
        company_name = itp_data['Company name']
        popup_name = f'<strong>{itp_data["Company name"]}</strong><br>{itp_data["Company address"]}'
        if not math.isnan(latitude) and not math.isnan(longitude):
            marker = folium.Marker(location=[latitude, longitude], popup=popup_name, tooltip=company_name)
            marker.add_to(map_size)

    text_load_state.text('Plotting ... Done!')
    
    show_choropleth = st.checkbox("Show Choropleth", value=False)
    if show_choropleth:
        plot_choropleth(map_size)

    components.html(map_size._repr_html_(), height=600, width=800)

