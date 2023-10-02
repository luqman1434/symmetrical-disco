import streamlit as st
import pandas as pd
import geopandas as gpd
import os
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")

st.set_page_config(page_title="Testing", page_icon="🗿")
st.markdown("# Testing Demo")


# Get the parent directory of the script's directory
parent_dir = os.path.dirname(os.path.dirname(__file__))

# MMU ITP List 13_9_9_11.xlsx
excel_file_path = os.path.join(parent_dir, 'MMU ITP List 13_9_9_11.xlsx')
xlsx = pd.read_excel(excel_file_path)

# itp_area_map.html
html_file_path = os.path.join(parent_dir, 'itp_area_map.html')
# html_file = pd.read_html(html_file_path)
with open(html_file_path, 'r') as f:
    html_file = f.read()
    # st.markdown(html_content, unsafe_allow_html=True)

# msia_district.geojson
geojson_file_path = os.path.join(parent_dir, 'msia_district.geojson')
geojson_file = gpd.read_file(geojson_file_path)


# Show the column names
st.markdown("### Column Names:")
st.write(xlsx.columns.tolist())
