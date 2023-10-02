# import streamlit as st
# import pandas as pd

# st.set_page_config(page_title="Testing", page_icon="😓")
# st.markdown("# Testing Demo")

import streamlit as st
import pandas as pd
from PIL import Image

# Define the path to the sample.png image
sample_image_path = '/Screenshot_360.jpg'  # Assuming sample.png is located in the parent directory

# Display the image
sample_image = Image.open(sample_image_path)
st.image(sample_image, caption='Sample Image', use_column_width=True)

st.set_page_config(page_title="Testing", page_icon="😓")
st.markdown("# Testing Demo")
