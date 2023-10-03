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
