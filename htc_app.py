import streamlit as st
from datetime import datetime
import pandas as pd
import calendar
import streamlit_authenticator as stauth
from streamlit_pages.add_payment_page import add_payment_page
from streamlit_pages.explore_complete_database_page import explore_complete_database_page
from streamlit_pages.update_parishioner_details_page import update_parishioner_details_page
from streamlit_pages.add_new_parishioner_page import add_new_parishioner_page
from streamlit_pages.explore_data_specific_parishioner_page import explore_data_specific_parishioner_page
from streamlit_pages.update_payment_details_page import update_payment_details_page
from streamlit_pages.utils import create_tables

# Main Streamlit app
def main():
    st.set_page_config(
        page_title="HTC application",
        page_icon="htcback-removebg-preview.png",
        layout="wide",
    )

    st.sidebar.markdown("<h1 style='text-align: center;'>Holy Trinity Church \n\n Pune</h1>", unsafe_allow_html=True)  

    st.sidebar.markdown(
        """
        <style>
            [data-testid=stSidebar] [data-testid=stImage]{
                .block-container {padding-top: 0 !important;}
                text-align: center; display: block; margin-left: auto; margin-right: auto; width: 30%;
            }
        </style>
        """, unsafe_allow_html=True
    )
    stimage = st.sidebar.image('images\htcbackground.png',width=100) # use_column_width=True

    create_tables()
    tab_options = ["Add Payment", "Update Payment details", "Explore Data Specific Parishioner", 
                   "Explore Complete Database", "Add New Parishioner", "Update Parishioner details"]
    selected_tab = st.sidebar.selectbox("Select Tab", tab_options)

    if selected_tab == "Add Payment":
        add_payment_page()

    elif selected_tab == "Update Payment details":
        update_payment_details_page()


    elif selected_tab == "Explore Data Specific Parishioner":
        explore_data_specific_parishioner_page()

    elif selected_tab == "Explore Complete Database":
        explore_complete_database_page()

    elif selected_tab == "Add New Parishioner":
        add_new_parishioner_page()

    elif selected_tab == "Update Parishioner details":
        update_parishioner_details_page()

    # elif selected_tab == "Database analysis":
    #     database_analysis_page()

if __name__ == '__main__':
   main()
    

    