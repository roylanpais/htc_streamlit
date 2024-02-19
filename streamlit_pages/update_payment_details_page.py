import streamlit as st
from .utils import create_connection
import pandas as pd
from datetime import datetime
import calendar

# Function to update payment details
def update_payment(receipt_number, field_values):
    conn, cursor = create_connection()
    cursor.execute(f"SELECT * FROM payments WHERE receipt_number = ?", (receipt_number,))
    payment = cursor.fetchone()
    if payment:
        # Construct the dynamic update query
        update_query = f'''
            UPDATE payments SET
            { ', '.join(f'{field} = ?' for field in field_values.keys())}
            WHERE receipt_number = ?
        '''
        cursor.execute(update_query, (*field_values.values(), receipt_number))
        
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

def update_payment_details_page():
    st.subheader("Update Payment details")
    receipt_number = st.text_input("Enter Receipt Number", key='update_payment_receipt_number', placeholder="Enter church support receipt number to Update Payment information...")
    field_values_update = dict()
    st.write("Select fields to update")
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        option_payment_date = st.checkbox('Payment Date')
    with col2:
        option_amount = st.checkbox('Amount')
    with col3:
        option_paid_till_date  = st.checkbox('Paid till date')

    if option_payment_date:
        field_values_update["payment_date"] = st.date_input("Payment Date", datetime.today())
    if option_amount:
        field_values_update["amount"] = st.number_input("Amount in INR", min_value=0, step=1)
    if option_paid_till_date:
        with st.expander('Paid till date'):
            report_year = st.selectbox("Year", range(datetime.now().year + 7, datetime.now().year -10, -1))
            report_month_str = st.radio("Month", calendar.month_name[1:], index=datetime.now().month - 1, horizontal=True)
            report_month = calendar.month_name[1:].index(report_month_str) + 1
        field_values_update["paid_till_date"] = datetime.strptime(f"{report_year}-{report_month:02d}-01", "%Y-%m-%d").date()
    
    if st.button("Update this receipt Payment Details"):
        if receipt_number:
            # if check_receipt_presence(warn_available = False, receipt_number = receipt_number):
            success = update_payment(receipt_number, field_values_update)
            if success:
                st.success("Payment details updated successfully!")
            else:
                st.warning("Receipt Number not found.")
        else:
            st.warning("Receipt Number is a required field.")