import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import math
import streamlit.components.v1 as components
from shapely.geometry import Point
from streamlit_folium import st_folium

# Define the function to read the Excel file
def read_file(filename, sheetname):
    excel_file = pd.ExcelFile(filename)
    data_d = excel_file.parse(sheet_name=sheetname)
    return data_d

def plot_markers(map_obj, data):
    for itp_data in data.to_dict(orient='records'):
        latitude = itp_data['map_latitude']
        longitude = itp_data['map_longitude']
        company_name = itp_data['Company name']
        data_str = company_name + ': ' + itp_data['Company address']
        popup_content = f"""
        <div>
            {company_name}<br>
            <a href="#" onclick="updateStreamlit('{data_str}'); return false;">Show in sidebar</a>
        </div>
        """
        if not math.isnan(latitude) and not math.isnan(longitude):
            folium.Marker(location=[latitude, longitude], popup=popup_content, tooltip=company_name).add_to(map_obj)

# JavaScript to communicate with Streamlit
js = """
<script>
    function updateStreamlit(data) {
        const Http = new XMLHttpRequest();
        const url = '/update_data?data=' + encodeURIComponent(data);
        Http.open("GET", url);
        Http.send();

        Http.onreadystatechange = (e) => {
            if(Http.readyState === 4 && Http.status === 200) {
                window.location.reload();
            }
        }
    }
</script>
"""

# ... Rest of your initial setup ...

st.title('Available ITP companies in Malaysia')
st.markdown(js, unsafe_allow_html=True) # Add the JS here

# ... Loading data ...

map_size = Figure(width=800, height=600)
map_my = folium.Map(location=[4.2105, 108.9758], zoom_start=6)
map_size.add_child(map_my)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

itp_list_state['geometry'] = itp_list_state.apply(lambda x: Point(x['map_longitude'], x['map_latitude']), axis=1)
itp_list_state = gpd.GeoDataFrame(itp_list_state, geometry='geometry')

selected_states = st.multiselect('Select States', itp_list_state['STATE'].unique())

filtered_data = itp_list_state[itp_list_state['STATE'].isin(selected_states)]

joined_data = gpd.sjoin(geojson_data, filtered_data, op="contains").groupby(["NAME_1", "NAME_2"]).size().reset_index(name="count")

merged_gdf = geojson_data.merge(joined_data, on=["NAME_1", "NAME_2"], how="left")
merged_gdf['count'].fillna(0, inplace=True)

threshold_scale = [0, 1, 2, 4, 8, 16, 32, 64, 128, 200, 300, 400] 

# Plot markers on the map
plot_markers(map_my, filtered_data)

show_choropleth = st.checkbox("Show Choropleth", value=False)
if show_choropleth:
    plot_choropleth(map_my, show_choropleth)

map_my.save('itp_area_map.html')
p = open('itp_area_map.html')
components.html(p.read(), 800, 480)

# Handle data from the JS function
if st.experimental_get_query_params().get('data'):
    data = st.experimental_get_query_params()['data'][0]
    st.sidebar.text(data)
