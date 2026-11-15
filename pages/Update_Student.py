
import streamlit as st
from db import connect_db
from auth import require_login

require_login()

st.title("✏️ Update Student")

conn = None
cur = None

# Fetch student records
try:
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT student_id, student_name, email, phone, department
        FROM students
        ORDER BY student_id
    """)

    students = cur.fetchall()

except Exception as e:
    st.error("Unable to load student records.")
    print("Database Error:", e)
    st.stop()

finally:
    if cur:
        cur.close()
    if conn:
        conn.close()


if not students:
    st.info("No students available. Please add a student first.")
    st.stop()


# Select student
selected = st.selectbox(
    "Select Student",
    students,
    format_func=lambda s: f"{s[1]} (ID: {s[0]})"
)

student_id = selected[0]

st.subheader("Edit Student Details")

with st.form(key=f"update_student_{student_id}"):

    name = st.text_input(
        "Student Name",
        value=selected[1] or ""
    )

    email = st.text_input(
        "Email",
        value=selected[2] or ""
    )

    phone = st.text_input(
        "Phone Number",
        value=selected[3] or ""
    )

    department = st.text_input(
        "Department",
        value=selected[4] or ""
    )

    submit = st.form_submit_button("Update Student")

    if submit:

        if not name.strip() or not email.strip() or not department.strip():
            st.warning("Please fill in all required fields.")

        elif phone and (not phone.isdigit() or len(phone) != 10):
            st.warning("Enter a valid 10-digit phone number.")

        else:
            conn = None
            cur = None

            try:
                conn = connect_db()
                cur = conn.cursor()

                query = """
                    UPDATE students
                    SET student_name = %s,
                        email = %s,
                        phone = %s,
                        department = %s
                    WHERE student_id = %s
                """

                cur.execute(
                    query,
                    (
                        name.strip(),
                        email.strip(),
                        phone.strip() or None,
                        department.strip(),
                        student_id
                    )
                )

                conn.commit()

                if cur.rowcount > 0:
                    st.success("Student details updated successfully!")
                else:
                    st.info("No changes were made.")

            except Exception as e:
                if conn:
                    conn.rollback()

                st.error("Unable to update student details.")
                print("Update Error:", e)

            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
