import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point

# Define the function to read the Excel file
def read_file(filename, sheetname):
    excel_file = pd.ExcelFile(filename)
    data_d = excel_file.parse(sheet_name=sheetname)
    return data_d

if __name__ == '__main__':
    st.title('Available ITP companies in Malaysia')

    file_input = 'MMU ITP List 13_9_9_11.xlsx'
    geojson_file = "msia_district.geojson"

    with open(geojson_file, encoding='utf-8', errors='ignore') as gj_f:
        geojson_data = gpd.read_file(gj_f)

    itp_list_state = read_file(file_input, 0)

    itp_list_state['geometry'] = itp_list_state.apply(lambda x: Point(x['map_longitude'], x['map_latitude']), axis=1)
    itp_list_state = gpd.GeoDataFrame(itp_list_state, geometry='geometry')

    selected_states = st.multiselect('Select States', itp_list_state['STATE'].unique())
    
    filtered_data = itp_list_state[itp_list_state['STATE'].isin(selected_states)]

    for itp_data in filtered_data.to_dict(orient='records'):
        latitude = itp_data['map_latitude']
        longitude = itp_data['map_longitude']
        company_name = itp_data['Company name']
        popup_name = f'<strong>{itp_data["Company name"]}</strong><br>{itp_data["Company address"]}'
        if not pd.isnull(latitude) and not pd.isnull(longitude):
            marker = folium.Marker(location=[latitude, longitude], popup=popup_name, tooltip=company_name)
            geojson_data = geojson_data.append({
                'geometry': Point(longitude, latitude),
                'Company name': company_name,
                'Company address': itp_data['Company address']
            }, ignore_index=True)

    m = folium.Map(location=[4.2105, 108.9758], zoom_start=6)
    folium.Choropleth(
        geo_data=geojson_data,
        name='choropleth',
        data=geojson_data,
        columns=['Company name', 'Company address'],
        key_on='feature.properties.Company name',
        fill_color='RdYlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='District Counts',
        highlight=False
    ).add_to(m)

    st.write(m)
