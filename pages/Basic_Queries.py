
import streamlit as st
import pandas as pd
from db import connect_db
from datetime import date
from auth import require_login

require_login()
st.title("📋 Basic Queries")

try:
    conn = connect_db()

    # 1. Display all students
    st.subheader("1. All Students")

    if st.button("Display All Students"):
        students = pd.read_sql(
            "SELECT * FROM students",
            conn
        )
        st.dataframe(students, hide_index=True, use_container_width=True)

    st.divider()

    # 2. Courses with fee greater than 5000
    st.subheader("2. Courses with Fee Greater Than ₹5000")

    if st.button("Show Courses"):
        courses = pd.read_sql(
            "SELECT * FROM courses WHERE fee > 5000",
            conn
        )
        st.dataframe(courses, hide_index=True, use_container_width=True)

    st.divider()

    # 3. List students by department
    st.subheader("3. Students by Department")

    departments = pd.read_sql(
        "SELECT DISTINCT department FROM students "
        "WHERE department IS NOT NULL ORDER BY department",
        conn
    )

    if not departments.empty:
        selected_department = st.selectbox(
            "Select Department",
            departments["department"].tolist()
        )

        students = pd.read_sql(
            """
            SELECT *
            FROM students
            WHERE department = %s
            """,
            conn,
            params=(selected_department,)
        )

        st.dataframe(students, hide_index=True, use_container_width=True)
    else:
        st.info("No departments found.")

    st.divider()

    # 4. Courses with duration more than 3 months
    st.subheader("4. Courses with Duration More Than 3 Months")

    if st.button("Show Long Duration Courses"):
        courses = pd.read_sql(
            """
            SELECT *
            FROM courses
            WHERE CAST(duration AS UNSIGNED) > 3
            """,
            conn
        )
        st.dataframe(courses, hide_index=True, use_container_width=True)

    st.divider()

    # 5. Students registered after a specific date
    st.subheader("5. Students Registered After a Specific Date")

    selected_date = st.date_input(
        "Select Registration Date",
        value=date(2026, 1, 1)
    )

    if st.button("Search Students"):
        students = pd.read_sql(
            """
            SELECT *
            FROM students
            WHERE registration_date > %s
            ORDER BY registration_date DESC
            """,
            conn,
            params=(selected_date,)
        )
        st.dataframe(students, hide_index=True, use_container_width=True)

    conn.close()

except Exception as e:
    st.error(f"Database error: {e}")
