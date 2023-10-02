import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Testing", page_icon="🗿")
st.markdown("# Testing Demo")


# Get the parent directory of the script's directory
parent_dir = os.path.dirname(os.path.dirname(__file__))
excel_file_path = os.path.join(parent_dir, 'MMU ITP List 13_9_9_11.xlsx')
data = pd.read_excel(excel_file_path)

st.write(data.columns.tolist())
