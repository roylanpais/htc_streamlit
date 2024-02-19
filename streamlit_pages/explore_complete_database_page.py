import streamlit as st
from streamlit_pages.utils import create_connection
import pandas as pd
from mitosheet.streamlit.v1 import spreadsheet
from streamlit_pages.utils import get_table_df

def explore_complete_database_page():
    st.subheader("Explore Database tables")

    database_selected = st.radio("Select database option to analyze", ["Parishioners Database", "Payments Database"], horizontal=True)

    if database_selected == "Parishioners Database":
        table_name = "parishioners"
    if database_selected == "Payments Database":
        table_name = "payments"
    spreadsheet(get_table_df(table_name))

    # col1, col2 = st.columns([1,1])
    # with col1:
    #     option_payment_date = st.checkbox("Parishioners Database")
    # with col2:
    #     option_amount = st.checkbox("Payments Database")
    
    # if option_payment_date:
    #     table_name = "parishioners"
    #     spreadsheet(get_table_df(table_name))
    # if option_amount:
    #     table_name = "payments"
    #     spreadsheet(get_table_df(table_name))
    