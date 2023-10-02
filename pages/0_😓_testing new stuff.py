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

# #revive here

# import streamlit as st
# import pandas as pd
# import os

# st.set_page_config(page_title="Testing", page_icon="😓")
# st.markdown("# Testing Demo")

# from PIL import Image

# # Get the parent directory of the script's directory
# parent_dir = os.path.dirname(os.path.dirname(__file__))

# # Define a list of file extensions you want to read
# extensions_to_read = ['.xlsx', '.geojson', '.html']

# # Initialize a list to store the names of the files
# file_names = []

# # Loop through files in the parent directory
# for file_name in os.listdir(parent_dir):
#     if any(file_name.endswith(ext) for ext in extensions_to_read):
#         # Add the file name to the list
#         file_names.append(file_name)

# # Display the list of files
# if file_names:
#     st.markdown("### List of Files:")
#     for file_name in file_names:
#         st.write(file_name)
# else:
#     st.write("No files with the specified extensions found in the parent directory.")


# excel_file_path = os.path.join(parent_dir, 'MMU ITP List 13_9_9_11.xlsx')
# data = pd.read_excel(excel_file_path)
# st.write(data.columns.tolist())


#start here
import streamlit as st

# Define the data as a list of dictionaries
data = [
    {'Intern': 'Aiman', 'Work Currently Doing': 'Implementation of current map inside streamlit, compilation of all current finished python file (error or otherwise) inside the implementation', 'Est time finish': 'Wednesday, 4/10'},
    {'Intern': 'Luqman', 'Work Currently Doing': 'Helping Sheikh on 13k dataset, addition of filters inside the streamlit application', 'Est time finish': 'Wednesday, 4/10'},
    {'Intern': 'Sheikh', 'Work Currently Doing': 'In charge of 13k dataset pre-processing', 'Est time finish': 'Unknown, est within 2 weeks'},
    {'Intern': 'Hamid', 'Work Currently Doing': 'Currently idle, cannot be reached', 'Est time finish': '????'},
    {'Intern': 'Abdullah', 'Work Currently Doing': "Haven't submitted last week's work yet, cannot be reached", 'Est time finish': '????'},
]

st.set_page_config(page_title="Testing", page_icon="😓")
st.markdown("# Vertical Table Demo")

# Display the data in a vertical format
for row in data:
    st.markdown(f"**Intern:** {row['Intern']}")
    st.markdown(f"**Work Currently Doing:** {row['Work Currently Doing']}")
    # st.markdown(f"**Est time finish:** {row['Est time finish']}\n---")
    st.markdown(f"**Work Currently Doing:** {row['Work Currently Doing']}")
