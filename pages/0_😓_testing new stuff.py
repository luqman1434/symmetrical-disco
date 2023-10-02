# import streamlit as st
# import pandas as pd

# st.set_page_config(page_title="Testing", page_icon="😓")
# st.markdown("# Testing Demo")

# import streamlit as st
# import pandas as pd
# from PIL import Image

# # Define the path to the sample.png image
# sample_image_path = '/Screenshot_360.jpg'  # Assuming sample.png is located in the parent directory

# # Display the image
# sample_image = Image.open(sample_image_path)
# st.image(sample_image, caption='Sample Image', use_column_width=True)

# st.set_page_config(page_title="Testing", page_icon="😓")
# st.markdown("# Testing Demo")

# import streamlit as st
# import pandas as pd
# from PIL import Image
# import os

# # Get the parent directory of the script's directory
# parent_dir = os.path.dirname(os.path.dirname(__file__))

# # Define the path to the sample.png image
# sample_image_path = os.path.join(parent_dir, 'Screenshot_360.jpg')

# # Check if the image file exists
# if os.path.exists(sample_image_path):
#     sample_image = Image.open(sample_image_path)
#     st.image(sample_image, caption='Sample Image', use_column_width=True)
# else:
#     st.write('Sample image not found.')

# st.set_page_config(page_title="Testing", page_icon="😓")
# st.markdown("# Testing Demo")


import streamlit as st
import pandas as pd

st.set_page_config(page_title="Testing", page_icon="😓")
st.markdown("# Testing Demo")

# Get the parent directory of the script's directory
parent_dir = os.path.dirname(os.path.dirname(__file__))

# Define the path to the sample.png image
sample_image_path = os.path.join(parent_dir, 'Screenshot_360.jpg')

# Check if the image file exists
if os.path.exists(sample_image_path):
    sample_image = Image.open(sample_image_path)
    st.image(sample_image, caption='Sample Image', use_column_width=True)
else:
    st.write('Sample image not found.')
