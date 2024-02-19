import streamlit as st
from datetime import datetime
from .utils import check_Parishioner_presence, create_connection
import calendar


# Function to add a new Parishioner to the database
def add_new_Parishioner(id, phone_number, name, doj, transferred):
    conn, cursor = create_connection()
    cursor.execute('INSERT OR IGNORE INTO Parishioners VALUES (?, ?, ?, ?, ?)',
                   (id, phone_number, name, doj, transferred))
    conn.commit()
    conn.close()

def add_new_parishioner_page():
    
    st.subheader("Add New Parishioner to the database")
    id = st.number_input("ID", value = None, min_value=0, step=1, placeholder="Create your unique HTC ID")
    phone_number = st.number_input("Phone Number", value = None, step=1, min_value=1000000000, max_value = 100000000000 , placeholder="Enter your Phone Number")
    name = st.text_input("Name", key='add_Parishioner_name', placeholder="Enter your name")
    # doj_month = st.selectbox("DOJ Month", calendar.month_name[1:], placeholder="Enter the month of joining the parish", index=None)        
    # doj_year = st.selectbox("DOJ Year", list(range(datetime.now().year, 1900, -1)), placeholder="Enter the year of joining the parish") 
    transferred = st.radio("Transferred", [ "No"])

    with st.expander('Date of Joining'):
        report_year = st.selectbox("Year",range(datetime.now().year, 1900, -1))
        report_month_str = st.radio("Month", calendar.month_name[1:], index=datetime.now().month - 1, horizontal=True)
        report_month = calendar.month_name[1:].index(report_month_str) + 1
    doj = datetime.strptime(f"{report_year}-{report_month:02d}-01", "%Y-%m-%d").date()

    if st.button("Add Parishioner"):
        if id and phone_number and name and transferred:
            add_new_Parishioner(id, phone_number, name, doj, transferred)
            st.success("Parishioner added successfully!")
        else:
            st.warning("All fields are required to be filled.")