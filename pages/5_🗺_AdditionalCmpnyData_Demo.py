import streamlit as st
import pandas as pd
import geopandas as gpd
import os
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")

st.set_page_config(page_title="AddCmpnyData Demo", page_icon="🗺")
st.markdown("# Additional Company Data Demo")
##
st.sidebar.header("Additional Company Data Demo")
st.write(
    """This iteration of the demo is the PushPin map which has the additional company description added into the pushpins. This has the benefit of showing the user more information when they click on the pushpins
    within the map shown"""
)
##

# Get the parent directory of the script's directory
parent_dir = os.path.dirname(os.path.dirname(__file__))
text_load_state = st.text('Reading files ...')


# MMU ITP List 13_9_9_11.xlsx
excel_file_path = os.path.join(parent_dir, 'MMU ITP List 13_9_9_11.xlsx')
xlsx = pd.read_excel(excel_file_path)

# itp_area_map.html
html_file_path = os.path.join(parent_dir, 'itp_area_map.html')
# html_file = pd.read_html(html_file_path)
with open(html_file_path, 'r') as f:
    html_file = f.read()

# msia_district.geojson
geojson_file_path = os.path.join(parent_dir, 'msia_district.geojson')
geojson_file = gpd.read_file(geojson_file_path)
text_load_state.text('Reading files ... Done!')

#file names for explanation
#geojson_file is read for the current geojson
#html_file is read for the current html
#xlsx is read for the current xlsx



#start here
from branca.element import Figure
import folium
from shapely.geometry import Point
import math
import streamlit.components.v1 as components

# import math
import json

# this specifically is one of the issues in the code
# color unsure what to import
# from turtle import color

# import warnings #done
from webbrowser import BackgroundBrowser

# import pandas as pd #done
# import geopandas as gpd #done
# import folium #done

from branca.element import Figure
from shapely.geometry import Point

# import streamlit as st #done
import streamlit.components.v1 as components
from streamlit_folium import st_folium

# # Import the sidebar function from sidebar.py
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

from PIL import Image
logo_image = Image.open('mmu-multimedia-university6129.png')


# st.image('mmu-multimedia-university6129.png', use_column_width=False, caption='', width=200, )
st.image(logo_image, use_column_width=False, caption='', width=200, )


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

# def read_file(filename, sheetname):
#     excel_file = pd.ExcelFile(filename)
#     data_d = excel_file.parse(sheet_name=sheetname)

#     return data_d

# if __name__ == '__main__':
#     st.title('Available ITP companies in Malaysia')
#     # Call the sidebar function to include it in your app
#     sidebar()
    

#     # Create an empty space in the sidebar to display company information
#     company_info_container = st.empty()

#     file_input = 'MMU ITP List 13_9_9_11.xlsx'
#     geojson_file = "msia_district.geojson"

#     text_load_state = st.text('Reading files ...')
#     with open(geojson_file) as gj_f:
#         geojson_data = gpd.read_file(gj_f)

#     itp_list_state = read_file(file_input, 0)
#     text_load_state.text('Reading files ... Done!')

#     map_size = Figure(width=800, height=600)
#     map_my = folium.Map(location=[4.2105, 108.9758], zoom_start=6)
#     map_size.add_child(map_my)

#     with warnings.catch_warnings():
#         warnings.simplefilter("ignore")
    
#     itp_list_state['geometry'] = itp_list_state.apply(lambda x: Point(x['map_longitude'], x['map_latitude']), axis=1)
#     itp_list_state = gpd.GeoDataFrame(itp_list_state, geometry='geometry')

#     joined_data = gpd.sjoin(geojson_data, itp_list_state, op="contains").groupby(["NAME_1", "NAME_2"]).size().reset_index(name="count")

#     merged_gdf = geojson_data.merge(joined_data, on=["NAME_1", "NAME_2"], how="left")
#     merged_gdf['count'].fillna(0, inplace=True)

#     threshold_scale = [0, 1, 2, 4, 8, 16, 32, 64, 128, 200, 300, 400] 

#     choropleth = folium.Choropleth(
#         geo_data=merged_gdf,
#         name='choropleth',
#         data=merged_gdf,
#         columns=['NAME_2', 'count'],
#         key_on='feature.properties.NAME_2',
#         fill_color='RdYlGn',
#         fill_opacity=0.7,
#         line_opacity=0.2,
#         threshold_scale=threshold_scale,
#         line_color='black',
#         legend_name='District Counts',
#         highlight=False  # Disable the darkened coloration when hovering
#     ).add_to(map_my)

#     folium.GeoJsonTooltip(fields=['NAME_1','NAME_2', 'count'], aliases=['State','District', 'Count']).add_to(choropleth.geojson)

#     text_load_state.text('Plotting ...')
#     for itp_data in itp_list_state.to_dict(orient='records'):
#         latitude = itp_data['map_latitude']
#         longitude = itp_data['map_longitude']
#         company_name = itp_data['Company name']
#         company_address = itp_data['Company address']
#         company_email = itp_data['Company Email'] 
#         company_tel = itp_data['Company Tel'] 
#         company_industry = itp_data['industry'] 
        
#         # Create a customized HTML popup with two sections
#         popup_content = f"""
#         <div>
#             <strong>{company_name}</strong><br>
#             <em>Address:</em> {company_address}<br>
#         </div>
#         <hr>
#         <div>
#             <em>Email:</em> {company_email}<br>
#             <em>Tel:</em> {company_tel}<br>
#             <em>Industry:</em> {company_industry}
#         </div>
#         """

#         if not math.isnan(latitude) and not math.isnan(longitude):
#             # Create a marker with the customized HTML popup
#             marker = folium.Marker(location=[latitude, longitude], tooltip=company_name)
#             marker.add_to(map_my)

#             # Add a click event to the marker to display a popup on click
#             folium.Popup(popup_content, max_width=400).add_to(marker)

#     # Save the map with markers and popups to an HTML file
#     map_my.save('itp_area_map.html')

#     # Display the HTML file in Streamlit
    


#     # for itp_data in itp_list_state.to_dict(orient='records'):
#     #     latitude = itp_data['map_latitude']
#     #     longitude = itp_data['map_longitude']
#     #     company_name = itp_data['Company name']
#     #     company_address = itp_data['Company address']
#     #     popup_name = '<strong>' + str(company_name) + '</strong>\n' + str(company_address)
#     #     if not math.isnan(latitude) and not math.isnan(longitude):
#     #         marker = folium.Marker(location=[latitude, longitude], popup=popup_name, tooltip=company_name)
#     #         marker.add_to(map_my)

#     #         # Create a function to update the sidebar with company information when marker is clicked
#     #         def update_sidebar(marker=marker, company_info_container=company_info_container):
#     #             company_info_container.write(f"**Company Name:** {company_name}")
#     #             company_info_container.write(f"**Company Address:** {company_address}")

#     #         # Add a click event to the marker
#     #         marker.add_to(map_my)
#     #         marker.add_child(folium.ClickForMarker(popup=update_sidebar))




# # Specify the file name
# file_name = "MMU ITP List 13_9_9_11.xlsx"

# try:
#     df = pd.read_excel(file_name, engine='openpyxl')
# except FileNotFoundError:
#     st.error(f"File '{file_name}' not found.")

# # Sidebar for state selection
# if df is not None:
#     selected_state = st.sidebar.selectbox("Select a State", df['STATE'].unique())
# else:
#     selected_state = None

# # Data processing
# if df is not None:
#     grouped_data = df.groupby(['STATE', 'CITY']).size().reset_index(name='CompanyCount')
#     grouped_data = grouped_data.sort_values(by=['STATE', 'CompanyCount'], ascending=[True, False])

#     # Create bar chart
#     if selected_state:
#         filtered_data = grouped_data[grouped_data['STATE'] == selected_state]
#         fig = px.bar(
#             filtered_data,
#             x='CompanyCount',
#             y='CITY',
#             orientation='h',
#             labels={'CITY': 'City', 'CompanyCount': 'Number of Companies'},
#             title=f'Company Distribution per City in {selected_state}'
            
#         )
#     else:
#         fig = px.bar(
#             grouped_data,
#             x='CompanyCount',
#             y='CITY',
#             orientation='h',
#             labels={'CITY': 'City', 'CompanyCount': 'Number of Companies'},
#             title='Company Distribution per City in Malaysia (Sorted by State and City)'
#         )

#     # Display the plotly figure
    
    
#     text_load_state.text('Plotting ... Done!')

#     map_my.save('itp_area_map.html')
#     # p = open('itp_area_map.html')
#     p = open('itp_area_map.html', 'r', encoding='utf-8')
#     components.html(p.read(), 1000, 600)
#     st.title('Company Per District')
#     st.plotly_chart(fig)
