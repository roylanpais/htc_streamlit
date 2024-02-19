import sqlite3
import streamlit as st
import pandas as pd

# Function to create SQLite connection and cursor
def create_connection():
    conn = sqlite3.connect('church_support.db')
    cursor = conn.cursor()
    return conn, cursor


def check_Parishioner_presence(warn_available, id_or_phone_option, id_or_phone):
    conn, cursor = create_connection()
    if id_or_phone_option == "ID":
        cursor.execute(f"SELECT * FROM Parishioners WHERE id = ?", (id_or_phone,))
    elif id_or_phone_option == "Phone_Number":
        cursor.execute(f"SELECT * FROM Parishioners WHERE phone_number = ?", (id_or_phone,))

    Parishioner = cursor.fetchone()
    if warn_available == True and Parishioner:
        st.warning(f"Parishioner data with the given {id_or_phone_option} already exists.")
        conn.close()
        return False
    elif warn_available == False and not Parishioner:
        st.warning(f"Parishioner data with the given {id_or_phone_option} not present in database. Kindly add a new Parishioner.")
        conn.close()
        return False
    else:
        conn.close()
        return True

def check_receipt_presence(warn_available, receipt_number):
    conn, cursor = create_connection()
    cursor.execute(f"SELECT * FROM payments WHERE receipt_number = ?", (receipt_number,))
    payment = cursor.fetchone()
    if warn_available == True and payment:
        st.warning(f"payment data with the given {receipt_number} already exists.")
        conn.close()
        return False
    if warn_available == False and not payment:
        st.warning(f"payment data with the given {receipt_number} not present in database. Kindly add a new Parishioner.")
        conn.close()
        return False
    else:
        conn.close()
        return True
    
# Function to display the complete database
def get_table_df(table_name):
    conn, cursor = create_connection()
    df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)
    conn.close()
    return df

# Function to create tables if they do not exist
def create_tables():
    conn, cursor = create_connection()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Parishioners (
            id INTEGER PRIMARY KEY,
            phone_number INTEGER NOT NULL,
            name TEXT NOT NULL,
            doj TEXT NOT NULL,
            transferred TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY,
            Parishioner_id INTEGER NOT NULL,
            payment_date TEXT NOT NULL,
            paid_till_date TEXT NOT NULL,
            amount INTEGER NOT NULL,
            receipt_number TEXT NOT NULL,
            FOREIGN KEY (Parishioner_id) REFERENCES Parishioners(id)
        )
    ''')

    conn.commit()
    conn.close()