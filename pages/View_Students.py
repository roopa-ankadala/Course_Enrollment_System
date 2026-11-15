
import streamlit as st
import pandas as pd
from db import connect_db
from auth import require_login

require_login()

st.title("👨‍🎓 View Students")

conn = None
cur = None

try:
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT student_id, student_name, email, phone, department
        FROM students
        ORDER BY student_id
    """)

    students = cur.fetchall()

    if not students:
        st.info("No students found. Please add students first.")

    else:
        df = pd.DataFrame(
            students,
            columns=[
                "Student ID",
                "Name",
                "Email",
                "Phone",
                "Department"
            ]
        )

        # Total Students
        st.metric("Total Students", len(df))

        # Search
        search = st.text_input("🔍 Search students")

        if search:
            df = df[
                df.astype(str).apply(
                    lambda row: row.str.contains(
                        search, case=False, regex=False
                    ).any(),
                    axis=1
                )
            ]

        st.subheader("Student Details")

        if df.empty:
            st.warning("No matching students found.")
        else:
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

except Exception as e:
    st.error("Unable to load student records.")
    print("Error:", e)

finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
