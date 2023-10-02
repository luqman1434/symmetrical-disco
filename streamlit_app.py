import streamlit as st

st.set_page_config(
    page_title="GLIE",
    page_icon="👨‍🎓",
)

st.write("# GLIE Internship Website 👨‍🎓")

st.sidebar.success("Select a function above.")

# st.markdown(
#     """
#     Streamlit is an open-source app framework built specifically for
#     Machine Learning and Data Science projects.
#     **👈 Select a demo from the sidebar** to see some examples
#     of what Streamlit can do!
#     ### Want to learn more?
#     - Check out [streamlit.io](https://streamlit.io)
#     - Jump into our [documentation](https://docs.streamlit.io)
#     - Ask a question in our [community
#         forums](https://discuss.streamlit.io)
#     ### See more complex demos
#     - Use a neural net to [analyze the Udacity Self-driving Car Image
#         Dataset](https://github.com/streamlit/demo-self-driving)
#     - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
# """
# )

st.markdown(
    """
    This is a website designed in September/October 2023 by GLIE Interns for our internship program. 
    The main function of this website is to provide a compiled list of companies which future students can look up in an interactive site, 
    and also providing other functionalities. 
    
    **👈 Select a page from the sidebar** to see some examples of what functionalities that we have!
    ### What functionalities that we have?
    - A map of Malaysia with pushpins showing the exact locations of each company
    - Graphs to provide a breakdown of the amount of companies inside each District and State
    ### Other functionalities to add?
    - A search function to find a list of companies for each:
        - Location (District/State)
        - Faculty
        - Others
    - A range based company locater which students can input (District/Lat-Long/etc) and find companies within a certain range close to them
    - Other features
"""
)
