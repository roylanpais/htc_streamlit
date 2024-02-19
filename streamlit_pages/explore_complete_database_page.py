import streamlit as st
from streamlit_pages.utils import create_connection
import pandas as pd
from mitosheet.streamlit.v1 import spreadsheet
from streamlit_pages.utils import get_table_df

def explore_complete_database_page():
    
    st.title('Tesla Stock Volume Analysis')
    
    database_selected = st.radio("Select database option to analyze", ["Parishioners Database", "Payments Databas"])
    if database_selected == "Parishioners Database":
        table_name = "parishioners"
    else:
        table_name = "payments"
    st.subheader("Explore Complete Database")
    spreadsheet(get_table_df(table_name))
