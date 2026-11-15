
import streamlit as st
import pandas as pd
from db import connect_db
from auth import require_login

require_login()
st.title("📊 Reports & Dashboard")

conn = None

try:
    conn = connect_db()

    # Total Counts
    students_count = pd.read_sql(
        "SELECT COUNT(*) AS total FROM students", conn
    ).iloc[0]["total"]

    courses_count = pd.read_sql(
        "SELECT COUNT(*) AS total FROM courses", conn
    ).iloc[0]["total"]

    enrollments_count = pd.read_sql(
        "SELECT COUNT(*) AS total FROM enrollments", conn
    ).iloc[0]["total"]

    # Student Details
    students = pd.read_sql(
        "SELECT * FROM students", conn
    )

    # Course Details
    courses = pd.read_sql(
        "SELECT * FROM courses", conn
    )

    # Detailed Enrollment Report
    enrollments = pd.read_sql("""
        SELECT
            e.enrollment_id,
            s.student_name,
            s.department,
            c.course_name,
            c.instructor,
            e.enrollment_date
        FROM enrollments e
        JOIN students s
            ON e.student_id = s.student_id
        JOIN courses c
            ON e.course_id = c.course_id
        ORDER BY e.enrollment_date DESC
    """, conn)

    # Course-wise Enrollment
    course_report = pd.read_sql("""
        SELECT
            c.course_name,
            COUNT(e.enrollment_id) AS total_enrollments
        FROM courses c
        LEFT JOIN enrollments e
            ON c.course_id = e.course_id
        GROUP BY c.course_id, c.course_name
        ORDER BY total_enrollments DESC
    """, conn)

    # Department-wise Enrollment
    department_report = pd.read_sql("""
        SELECT
            s.department,
            COUNT(e.enrollment_id) AS total_enrollments
        FROM students s
        LEFT JOIN enrollments e
            ON s.student_id = e.student_id
        GROUP BY s.department
        ORDER BY total_enrollments DESC
    """, conn)

    # Monthly Enrollment Trend
    monthly_report = pd.read_sql("""
        SELECT
            DATE_FORMAT(enrollment_date, '%Y-%m') AS month,
            COUNT(*) AS total_enrollments
        FROM enrollments
        GROUP BY DATE_FORMAT(enrollment_date, '%Y-%m')
        ORDER BY month
    """, conn)

    # Course Capacity Report
    capacity_report = pd.read_sql("""
        SELECT
            c.course_name,
            c.capacity,
            COUNT(e.enrollment_id) AS enrolled,
            c.capacity - COUNT(e.enrollment_id) AS available_seats
        FROM courses c
        LEFT JOIN enrollments e
            ON c.course_id = e.course_id
        GROUP BY c.course_id, c.course_name, c.capacity
        ORDER BY c.course_name
    """, conn)

except Exception as e:
    st.error("Unable to load reports.")
    print("Database Error:", e)
    st.stop()

finally:
    if conn:
        conn.close()


# KPI Metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Students", students_count)
col2.metric("Total Courses", courses_count)
col3.metric("Total Enrollments", enrollments_count)

st.divider()


# Course-wise Enrollment Chart
st.subheader("📚 Course-wise Enrollments")

if not course_report.empty:
    st.bar_chart(
        course_report,
        x="course_name",
        y="total_enrollments"
    )
else:
    st.info("No course data available.")


# Department-wise Enrollment Chart
st.subheader("🏢 Department-wise Enrollments")

if not department_report.empty:
    st.bar_chart(
        department_report,
        x="department",
        y="total_enrollments"
    )
else:
    st.info("No department data available.")


# Monthly Enrollment Trend
st.subheader("📈 Monthly Enrollment Trend")

if not monthly_report.empty:
    st.line_chart(
        monthly_report,
        x="month",
        y="total_enrollments"
    )
else:
    st.info("No enrollment history available.")


st.divider()


# Course Capacity Chart
st.subheader("🎯 Course Capacity")

if not capacity_report.empty:
    st.bar_chart(
        capacity_report,
        x="course_name",
        y=["enrolled", "available_seats"]
    )
else:
    st.info("No course capacity data available.")


st.divider()


# Student Details
st.subheader("👨‍🎓 Students")

st.dataframe(
    students,
    hide_index=True,
    use_container_width=True
)


# Course Details
st.subheader("📚 Courses")

st.dataframe(
    courses,
    hide_index=True,
    use_container_width=True
)


# Course Capacity Details
st.subheader("🎯 Course Capacity Details")

st.dataframe(
    capacity_report,
    hide_index=True,
    use_container_width=True
)


# Enrollment Details
st.subheader("📋 Enrollment Report")

if not enrollments.empty:
    st.dataframe(
        enrollments,
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("No enrollment records found.")
