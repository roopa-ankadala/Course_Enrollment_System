
import streamlit as st
from db import connect_db
from datetime import date
from auth import require_login

require_login()
st.title("Enroll Student")

conn = None
cur = None

try:
    conn = connect_db()
    cur = conn.cursor()

    # Fetch students
    cur.execute("""
        SELECT student_id, student_name
        FROM students
        ORDER BY student_name
    """)
    students = cur.fetchall()

    # Fetch courses with enrollment counts
    cur.execute("""
        SELECT
            c.course_id,
            c.course_name,
            c.capacity,
            COUNT(e.enrollment_id) AS enrolled
        FROM courses c
        LEFT JOIN enrollments e
            ON c.course_id = e.course_id
        GROUP BY c.course_id, c.course_name, c.capacity
        ORDER BY c.course_name
    """)
    courses = cur.fetchall()

except Exception as e:
    st.error("Unable to load data.")
    print("Database Error:", e)
    st.stop()

finally:
    if cur:
        cur.close()
    if conn:
        conn.close()


if not students:
    st.warning("Please add a student first.")
    st.stop()

if not courses:
    st.warning("Please add a course first.")
    st.stop()


# Student selection
selected_student = st.selectbox(
    "Select Student",
    students,
    format_func=lambda s: f"{s[1]} (ID: {s[0]})"
)

# Course selection
selected_course = st.selectbox(
    "Select Course",
    courses,
    format_func=lambda c: (
        f"{c[1]} - {c[3]}/{c[2]} enrolled "
        f"({c[2] - c[3]} seats available)"
    )
)

if st.button("Enroll"):

    student_id = selected_student[0]
    course_id = selected_course[0]

    conn = None
    cur = None

    try:
        conn = connect_db()
        conn.start_transaction()
        cur = conn.cursor()

        # Lock course row and check its capacity
        cur.execute("""
            SELECT capacity
            FROM courses
            WHERE course_id = %s
            FOR UPDATE
        """, (course_id,))

        result = cur.fetchone()

        if result is None:
            st.error("Selected course no longer exists.")

        else:
            capacity = result[0]

            # Check duplicate enrollment
            cur.execute("""
                SELECT enrollment_id
                FROM enrollments
                WHERE student_id = %s
                AND course_id = %s
            """, (student_id, course_id))

            duplicate = cur.fetchone()

            if duplicate:
                st.warning("Student is already enrolled in this course.")

            else:
                # Count current enrollments
                cur.execute("""
                    SELECT COUNT(*)
                    FROM enrollments
                    WHERE course_id = %s
                """, (course_id,))

                enrolled_count = cur.fetchone()[0]

                if enrolled_count >= capacity:
                    st.error("Course is full! No seats available.")

                else:
                    cur.execute("""
                        INSERT INTO enrollments
                        (student_id, course_id, enrollment_date)
                        VALUES (%s, %s, %s)
                    """, (student_id, course_id, date.today()))

                    conn.commit()
                    st.success("Student Enrolled Successfully!")

    except Exception as e:
        if conn:
            conn.rollback()

        st.error("Enrollment failed. Please try again.")
        print("Enrollment Error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
