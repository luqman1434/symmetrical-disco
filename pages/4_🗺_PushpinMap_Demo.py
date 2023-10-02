
# import streamlit as st
# import pandas as pd
# import altair as alt
# from urllib.error import URLError

# st.set_page_config(page_title="Pushpin Map", page_icon="🗺")

# st.markdown("# Pushpin Map Demo")
# st.sidebar.header("Pushpin Map")
# # st.write(
# #     """This demo shows how to use `st.write` to visualize Pandas DataFrames.
# # (Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
# # )


# # @st.cache_data
# # def get_UN_data():
# #     AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
# #     df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
# #     return df.set_index("Region")


# # try:
# #     df = get_UN_data()
# #     countries = st.multiselect(
# #         "Choose countries", list(df.index), ["China", "United States of America"]
# #     )
# #     if not countries:
# #         st.error("Please select at least one country.")
# #     else:
# #         data = df.loc[countries]
# #         data /= 1000000.0
# #         st.write("### Gross Agricultural Production ($B)", data.sort_index())

# #         data = data.T.reset_index()
# #         data = pd.melt(data, id_vars=["index"]).rename(
# #             columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
# #         )
# #         chart = (
# #             alt.Chart(data)
# #             .mark_area(opacity=0.3)
# #             .encode(
# #                 x="year:T",
# #                 y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
# #                 color="Region:N",
# #             )
# #         )
# #         st.altair_chart(chart, use_container_width=True)
# # except URLError as e:
# #     st.error(
# #         """
# #         **This demo requires internet access.**
# #         Connection error: %s?
# #     """

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pushpin Map Demo", page_icon="🗺")
st.markdown("# Pushpin Map Demo")

##########################################

import math
import json
# from turtle import color
import warnings
from webbrowser import BackgroundBrowser

# import pandas as pd
import geopandas as gpd
import folium

from branca.element import Figure
from shapely.geometry import Point

# import streamlit as st
import streamlit.components.v1 as components
# from streamlit_folium import st_folium

# Import the sidebar function from sidebar.py
# from sidebar import sidebar
import plotly.express as px

st.markdown(
    """
    <style>
    body {
        background-image: url('background.jpg'); 
        background-repeat: no-repeat;
        background-size: cover;
        background-attachment: fixed;
    }

    .logo {
        position: absolute;
        top: 20px;
        right: 20px;
        width: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
 
st.image('../mmu-multimedia-university6129.png', use_column_width=False, caption='', width=200, )

# 3.16000, 101.71000 : Kuala Lumpur

def set_background_color(color):
    """
    Set the background color of the Streamlit app.
    
    Args:
        color (str): The background color in CSS format (e.g., 'lightblue').
    """
    # Generate HTML code to set the background color
    html_code = f"""
    <style>
    body {{
        background-color: {color};
    }}
    </style>
    """
    
    # Apply the HTML code using st.markdown
    st.markdown(html_code, unsafe_allow_html=True)

# Use the set_background_color function to set the background color
set_background_color('lightblue')

def read_file(filename, sheetname):
    excel_file = pd.ExcelFile(filename)
    data_d = excel_file.parse(sheet_name=sheetname)

    return data_d

if __name__ == '__main__':
    st.title('Available ITP companies in Malaysia')
    # Call the sidebar function to include it in your app
    sidebar()
    

    # Create an empty space in the sidebar to display company information
    company_info_container = st.empty()

    file_input = 'MMU ITP List 13_9_9_11.xlsx'
    geojson_file = "msia_district.geojson"

    text_load_state = st.text('Reading files ...')
    with open(geojson_file) as gj_f:
        geojson_data = gpd.read_file(gj_f)

    itp_list_state = read_file(file_input, 0)
    text_load_state.text('Reading files ... Done!')

    map_size = Figure(width=800, height=600)
    map_my = folium.Map(location=[4.2105, 108.9758], zoom_start=6)
    map_size.add_child(map_my)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    
    itp_list_state['geometry'] = itp_list_state.apply(lambda x: Point(x['map_longitude'], x['map_latitude']), axis=1)
    itp_list_state = gpd.GeoDataFrame(itp_list_state, geometry='geometry')

    joined_data = gpd.sjoin(geojson_data, itp_list_state, op="contains").groupby(["NAME_1", "NAME_2"]).size().reset_index(name="count")

    merged_gdf = geojson_data.merge(joined_data, on=["NAME_1", "NAME_2"], how="left")
    merged_gdf['count'].fillna(0, inplace=True)

    threshold_scale = [0, 1, 2, 4, 8, 16, 32, 64, 128, 200, 300, 400] 

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
        highlight=False  # Disable the darkened coloration when hovering
    ).add_to(map_my)

    folium.GeoJsonTooltip(fields=['NAME_1','NAME_2', 'count'], aliases=['State','District', 'Count']).add_to(choropleth.geojson)

    text_load_state.text('Plotting ...')
    for itp_data in itp_list_state.to_dict(orient='records'):
        latitude = itp_data['map_latitude']
        longitude = itp_data['map_longitude']
        company_name = itp_data['Company name']
        company_address = itp_data['Company address']
        company_email = itp_data['Company Email'] 
        company_tel = itp_data['Company Tel'] 
        company_industry = itp_data['industry'] 
        
        # Create a customized HTML popup with two sections
        popup_content = f"""
        <div>
            <strong>{company_name}</strong><br>
            <em>Address:</em> {company_address}<br>
        </div>
        <hr>
        <div>
            <em>Email:</em> {company_email}<br>
            <em>Tel:</em> {company_tel}<br>
            <em>Industry:</em> {company_industry}
        </div>
        """

        if not math.isnan(latitude) and not math.isnan(longitude):
            # Create a marker with the customized HTML popup
            marker = folium.Marker(location=[latitude, longitude], tooltip=company_name)
            marker.add_to(map_my)

            # Add a click event to the marker to display a popup on click
            folium.Popup(popup_content, max_width=400).add_to(marker)

    # Save the map with markers and popups to an HTML file
    map_my.save('itp_area_map.html')

# Specify the file name
file_name = "MMU ITP List 13_9_9_11.xlsx"

try:
    df = pd.read_excel(file_name, engine='openpyxl')
except FileNotFoundError:
    st.error(f"File '{file_name}' not found.")

# Sidebar for state selection
if df is not None:
    selected_state = st.sidebar.selectbox("Select a State", df['STATE'].unique())
else:
    selected_state = None

# Data processing
if df is not None:
    grouped_data = df.groupby(['STATE', 'CITY']).size().reset_index(name='CompanyCount')
    grouped_data = grouped_data.sort_values(by=['STATE', 'CompanyCount'], ascending=[True, False])

    # Create bar chart
    if selected_state:
        filtered_data = grouped_data[grouped_data['STATE'] == selected_state]
        fig = px.bar(
            filtered_data,
            x='CompanyCount',
            y='CITY',
            orientation='h',
            labels={'CITY': 'City', 'CompanyCount': 'Number of Companies'},
            title=f'Company Distribution per City in {selected_state}'
            
        )
    else:
        fig = px.bar(
            grouped_data,
            x='CompanyCount',
            y='CITY',
            orientation='h',
            labels={'CITY': 'City', 'CompanyCount': 'Number of Companies'},
            title='Company Distribution per City in Malaysia (Sorted by State and City)'
        )

    # Display the plotly figure
    text_load_state.text('Plotting ... Done!')

    map_my.save('itp_area_map.html')
    p = open('itp_area_map.html', 'r', encoding='utf-8')
    components.html(p.read(), 1000, 600)
    st.title('Company Per District')
    st.plotly_chart(fig)
