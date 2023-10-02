import streamlit as st
import pandas as pd

st.set_page_config(page_title="Testing", page_icon="😓")
st.markdown("# Testing Demo")

from PIL import Image
import os

# Get the parent directory of the script's directory
parent_dir = os.path.dirname(os.path.dirname(__file__))

# Define the path to the sample.png image
sample_image_path = os.path.join(parent_dir, 'mmu-multimedia-university6129.png')

# Check if the image file exists
if os.path.exists(sample_image_path):
    sample_image = Image.open(sample_image_path)
    st.image(sample_image, caption='Sample Image', use_column_width=True)
else:
    st.write('Sample image not found.')
