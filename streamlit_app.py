import streamlit as st

st.set_page_config(
    page_title="GLIE",
   page_icon="👨‍🎓",
 )

st.write("# GLIE Internship Website 👨‍🎓")

st.sidebar.success("Select a function above.")

st.markdown(
    """
    This is a website designed in September/October 2023 by GLIE Interns for our internship program. 
    The main function of this website is to provide a compiled list of companies which future students can look up in an interactive site, 
    and also providing other functionalities. 
    
    **👈 Select a page from the sidebar** to see some examples of what functionalities that we have!
    ### What functionalities that we have currently?
    - A map of Malaysia with pushpins showing the exact locations of each company
    - Filter the pushpin map by States and ability to toggle choropleth
    - Graphs to provide a breakdown of the amount of companies inside each District and State
    - A function to search for ITP companies in our dataset and filter them by State.
    - Search for companies within a certain distance from its coordinates.
    - Function to geocode any input location
    
    ### Other functionalities to add?
    - A search function to find a list of companies for each:
        - Location (District/State)
        - Faculty
        - Others
    - A range based company locater which students can input (District/Lat-Long/etc) and find companies within a certain range close to them
    - Other features to be discussed
"""
)
