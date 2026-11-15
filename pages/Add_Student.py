
import streamlit as st
from db import connect_db
from auth import require_login

require_login()

st.title("👨‍🎓 Add Student")

name = st.text_input("Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
dept = st.text_input("Department")

if st.button("Submit"):

    if not name or not email or not phone or not dept:
        st.warning("Please fill all fields.")

    elif not phone.isdigit() or len(phone) != 10:
        st.warning("Enter a valid 10-digit phone number.")

    else:
        conn = None
        cur = None

        try:
            conn = connect_db()
            cur = conn.cursor()

            query = """
                INSERT INTO students
                (student_name, email, department, phone)
                VALUES (%s, %s, %s, %s)
            """

            cur.execute(query, (name, email, dept, phone))
            conn.commit()

            st.success("Student Added Successfully!")

        except Exception as e:
            if conn:
                conn.rollback()
            st.error(f"Error: {e}")

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
