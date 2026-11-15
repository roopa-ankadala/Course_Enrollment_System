
import streamlit as st
import pandas as pd
from db import connect_db
from auth import require_login

require_login()
st.title("🔗 SQL Joins")

conn = None

try:
    conn = connect_db()

    # 1. Student names with enrolled courses
    st.subheader("1. Students with Enrolled Courses")

    if st.button("Show Student Courses"):
        query = """
            SELECT
                s.student_id,
                s.student_name,
                c.course_name
            FROM students s
            INNER JOIN enrollments e
                ON s.student_id = e.student_id
            INNER JOIN courses c
                ON e.course_id = c.course_id
            ORDER BY s.student_name
        """

        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True, use_container_width=True)

    st.divider()

    # 2. Display course with instructor
    st.subheader("2. Courses with Instructors")

    if st.button("Show Courses and Instructors"):
        query = """
            SELECT
                c.course_id,
                c.course_name,
                i.instructor_name
            FROM courses c
            LEFT JOIN instructors i
                ON c.instructor_id = i.instructor_id
        """

        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True, use_container_width=True)

    st.divider()

    # 3. Enrollment details with student and course
    st.subheader("3. Complete Enrollment Details")

    if st.button("Show Enrollment Details"):
        query = """
            SELECT
                e.enrollment_id,
                s.student_name,
                c.course_name,
                e.enrollment_date
            FROM enrollments e
            INNER JOIN students s
                ON e.student_id = s.student_id
            INNER JOIN courses c
                ON e.course_id = c.course_id
            ORDER BY e.enrollment_date DESC
        """

        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True, use_container_width=True)

    st.divider()

    # 4. Students with department names
    st.subheader("4. Students with Department Names")

    if st.button("Show Student Departments"):
        query = """
            SELECT
                s.student_id,
                s.student_name,
                d.department_name
            FROM students s
            LEFT JOIN departments d
                ON s.department_id = d.department_id
            ORDER BY s.student_name
        """

        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True, use_container_width=True)

    st.divider()

    # 5. Instructor handling each course
    st.subheader("5. Instructor Handling Each Course")

    if st.button("Show Instructor Assignments"):
        query = """
            SELECT
                i.instructor_id,
                i.instructor_name,
                c.course_name
            FROM instructors i
            INNER JOIN courses c
                ON i.instructor_id = c.instructor_id
            ORDER BY i.instructor_name
        """

        df = pd.read_sql(query, conn)
        st.dataframe(df, hide_index=True, use_container_width=True)

except Exception as e:
    st.error(f"Database error: {e}")

finally:
    if conn:
        conn.close()
