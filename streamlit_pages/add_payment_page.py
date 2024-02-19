import streamlit as st
from datetime import datetime
from .utils import check_Parishioner_presence, create_connection
import calendar


# Function to add a new payment to the database
def add_payment(id_or_phone_option, id_or_phone, payment_date, paid_till_date , amount, receipt_number):
    conn, cursor = create_connection()
    cursor.execute(f"SELECT * FROM Parishioners WHERE {id_or_phone_option} = ?", (id_or_phone,))
    Parishioner = cursor.fetchone()

    if Parishioner:
        cursor.execute('INSERT INTO payments (Parishioner_id, payment_date, paid_till_date, amount, receipt_number) VALUES (?, ?, ?, ?, ?)',
                       (Parishioner[0], payment_date, paid_till_date, amount, receipt_number))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False


def add_payment_page():
    st.subheader("Add Payment")
    id_or_phone_option = st.radio("Select Option", ["ID", "Phone_Number"])
    id_or_phone = st.number_input(f"Enter {id_or_phone_option}", step=1, value= None, key='add_payment_id_or_phone',  placeholder=f"Enter {id_or_phone_option} as unique identifier")
    if id_or_phone:
        check_Parishioner_presence(warn_available = False, id_or_phone_option = id_or_phone_option, id_or_phone = id_or_phone)
    payment_date = st.date_input("Payment Date", datetime.today())

    # payment_month = st.selectbox("Paying upto Month", calendar.month_name[1:], index=None,    placeholder="Select the month upto which payment is being done...",)
    # payment_year = st.selectbox("Paying Upto Year", list(range(2020, 2036)), index=None,    placeholder="Select the year upto which payment is being done...",)
    amount = st.number_input("Amount in INR",value= None, min_value=0, step=500, placeholder="Enter amount paid to church support...")
    receipt_number = st.text_input("Receipt Number", key='add_payment_receipt_number',  placeholder="Enter church support receipt_number...")
    with st.expander('Paid till date'):
        report_year = st.selectbox("Year",range(datetime.now().year,  datetime.now().year -10, -1))
        report_month_str = st.radio("Month", calendar.month_name[1:], index=datetime.now().month - 1, horizontal=True)
        report_month = calendar.month_name[1:].index(report_month_str) + 1
    paid_till_date = datetime.strptime(f"{report_year}-{report_month:02d}-01", "%Y-%m-%d").date()

    if st.button("Add Payment"):
        if id_or_phone and payment_date and paid_till_date and amount and receipt_number:
            success = add_payment(id_or_phone_option, id_or_phone, payment_date, paid_till_date, amount, receipt_number)
            if success:
                st.success("Payment added successfully! Kindly collect receipt from the HTC church office")
            else:
                st.warning("Parishioner data not present in database. Kindly add a new Parishioner.")
        else:
            st.warning("All fields are required to be filled.")
