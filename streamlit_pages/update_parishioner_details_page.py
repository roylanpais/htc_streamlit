import streamlit as st
from datetime import datetime
from .utils import create_connection
import calendar

# Function to update Parishioner details
def update_Parishioner(id_or_phone_option, id_or_phone, field_values):
    conn, cursor = create_connection()
    cursor.execute(f"SELECT * FROM Parishioners WHERE {id_or_phone_option} = ?", (id_or_phone,))
    Parishioner = cursor.fetchone()
    if Parishioner:
        update_query = f'''
            UPDATE Parishioners SET
            { ', '.join(f'{field} = ?' for field in field_values.keys())}
            WHERE {id_or_phone_option} = ?
        '''
        cursor.execute(update_query, (*field_values.values(), id_or_phone))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

def update_parishioner_details_page():
    st.subheader("Update Parishioner details")
    id_or_phone_option = st.radio("Select Option", ["ID", "Phone Number"])
    id_or_phone = st.number_input(f"Enter {id_or_phone_option}", value = None, min_value=0, step=1, placeholder=f"Enter {id_or_phone_option}")
    field_values_update = dict()
    st.write("Select fields to update")
    print("hi")
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        option_new_id = st.checkbox('ID')
    with col2:
        option_new_phone_number  = st.checkbox('Phone number')
    with col3:
        option_new_name = st.checkbox('Name')
    with col4:
        option_new_doj = st.checkbox('Date of Joining')
    with col5:
        option_new_shifted = st.checkbox('shifted')

    if option_new_id:
        field_values_update["id"] = (st.number_input("New ID", value = None, min_value=0, step=1, placeholder="Create your updated unique HTC ID"))
    if option_new_phone_number:
        field_values_update["phone_number"] = (st.number_input("Phone Number", value = None, min_value=1000000000,step=1, max_value = 100000000000 , placeholder = "Enter your updated Phone Number"))
    if option_new_name:
        field_values_update["name"] = st.text_input("New Name", key='update_Parishioner_name', placeholder="Enter your name")
    if option_new_shifted:
        field_values_update["transferred"] = st.radio("Shifted", ["Yes", "No"])
    if option_new_doj:
        with st.expander('Date of Joining'):
            report_year = st.selectbox("Year",range(datetime.now().year, 1900, -1))
            report_month_str = st.radio("Month", calendar.month_name[1:], index=datetime.now().month - 1, horizontal=True)
            report_month = calendar.month_name[1:].index(report_month_str) + 1
        field_values_update["doj"] = datetime.strptime(f"{report_year}-{report_month:02d}-01", "%Y-%m-%d").date()

    if st.button("Update Parishioner Details"):
        if id_or_phone:
            # if check_receipt_presence(warn_available = False, receipt_number = receipt_number):
            success = update_Parishioner(id_or_phone_option, id_or_phone, field_values_update)
            if success:
                st.success("Parishioner details updated successfully!")
            else:
                st.warning("ID/Phone Number not found.")
        else:
            st.warning("ID/Phone Number is a required field.")
