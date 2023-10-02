# import streamlit as st
# import pandas as pd

# st.set_page_config(page_title="Testing", page_icon="😓")
# st.markdown("# Testing Demo")

# from PIL import Image
# import os

# # Get the parent directory of the script's directory
# parent_dir = os.path.dirname(os.path.dirname(__file__))

# # Define the path to the sample.png image
# sample_image_path = os.path.join(parent_dir, 'mmu-multimedia-university6129.png')

# # Check if the image file exists
# if os.path.exists(sample_image_path):
#     sample_image = Image.open(sample_image_path)
#     st.image(sample_image, caption='Sample Image', use_column_width=True)
# else:
#     st.write('Sample image not found.')


import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Testing", page_icon="😓")
st.markdown("# Testing Demo")

from PIL import Image

# Get the parent directory of the script's directory
parent_dir = os.path.dirname(os.path.dirname(__file__))

# Define a list of file extensions you want to read
extensions_to_read = ['.xlsx', '.json', '.html']

# Initialize a list to store the names of the files
file_names = []

# Loop through files in the parent directory
for file_name in os.listdir(parent_dir):
    if any(file_name.endswith(ext) for ext in extensions_to_read):
        # Add the file name to the list
        file_names.append(file_name)

# Display the list of files
if file_names:
    st.markdown("### List of Files:")
    for file_name in file_names:
        st.write(file_name)
else:
    st.write("No files with the specified extensions found in the parent directory.")
