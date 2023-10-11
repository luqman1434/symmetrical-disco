import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import math
from shapely.geometry import Point
from streamlit_folium import st_folium

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
        folium.GeoJsonTooltip(fields=['NAME_1', 'NAME_2', 'count'], aliases=['State', 'District', 'Count']).add_to(choropleth.geojson)

st.title('Available ITP companies in Malaysia')
file_input = 'MMU ITP List 13_9_9_11.xlsx'
geojson_file = "msia_district.geojson"

with open(geojson_file, encoding='utf-8', errors='ignore') as gj_f:
    geojson_data = gpd.read_file(gj_f)

itp_list_state = read_file(file_input, 0)
map_my = folium.Map(location=[4.2105, 108.9758], zoom_start=6)

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
    popup_content = """
    <strong>{}</strong><br>{}<br>
    <a href="?company={}" target="_self">Show Details</a>
    """.format(itp_data['Company name'], itp_data['Company address'], company_name)
    popup = folium.Popup(popup_content, max_width=300)
    folium.Marker(location=[latitude, longitude], popup=popup, tooltip=company_name).add_to(map_my)

show_choropleth = st.checkbox("Show Choropleth", value=False)
if show_choropleth:
    plot_choropleth(map_my)

st_folium(map_my)

# Check if there's a 'company' parameter in the URL
params = st.experimental_get_query_params()
selected_company = params.get("company")
if selected_company:
    selected_company = selected_company[0]  # Get the first item from the list
    company_details = filtered_data[filtered_data['Company name'] == selected_company].iloc[0]
    st.sidebar.text("Company name: " + company_details['Company name'])
    st.sidebar.text("Company address: " + company_details['Company address'])
    # ... Display other details ...
# ... Display other details ...

# For the purpose of demonstration, if there are more columns in the `filtered_data`, you can display them as well. For instance:
    st.sidebar.text("Company phone: " + str(company_details.get('Company phone', 'N/A')))
    st.sidebar.text("Company email: " + str(company_details.get('Company email', 'N/A')))
    # You can continue to add more fields as needed.

# Additional Streamlit elements for user interactivity or information display can follow here, such as:
st.markdown("### Instructions")
st.write("To view details of a specific company, click on the 'Show Details' link in the popup of each marker. The detailed information will then appear in the sidebar.")

# Finally, if you want to give an option for users to reset the selection (clear the sidebar details), you can add a button:
if st.button("Reset Selection"):
    # This will clear the URL parameters and hence clear the sidebar details upon refresh.
    st.experimental_set_query_params()
    st.experimental_rerun()
