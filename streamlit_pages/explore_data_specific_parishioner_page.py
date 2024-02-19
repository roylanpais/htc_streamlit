import streamlit as st
from .utils import create_connection
import pandas as pd

# Function to get Parishioner data based on name, id, or phone number
def get_Parishioner_data(search_key, search_value):
    conn, cursor = create_connection()
    cursor.execute(f"SELECT * FROM Parishioners WHERE {search_key} = ?", (search_value,))
    Parishioner_data = cursor.fetchall()
    conn.close()
    return Parishioner_data


def explore_data_specific_parishioner_page():
    st.subheader("Explore Data for Specific Parishioner")
    search_option = st.radio("Search by", ["Parishioner Name", "ID", "Phone Number"])

    if search_option == "Parishioner Name":
        search_key = "name"
    elif search_option == "ID":
        search_key = "id"
    else:
        search_key = "phone_number"

    search_value = st.text_input(f"Enter {search_option}", key='explore_data_search_value')

    if st.button("Explore Data"):
        if search_value:
            Parishioner_data = get_Parishioner_data(search_key, search_value)
            if Parishioner_data:
                st.write(pd.DataFrame(Parishioner_data, columns=["ID", "Phone Number", "Name", "DOJ", "Transferred"]))
            else:
                st.warning(f"No data found for {search_option}: {search_value}")
        else:
            st.warning(f"{search_option} is a required field.")