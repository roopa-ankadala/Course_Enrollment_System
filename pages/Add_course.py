
import streamlit as st
from db import connect_db
from auth import require_login

require_login()
st.title("Add Course")

course_name = st.text_input("Course Name")
instructor = st.text_input("Instructor")
duration = st.text_input("Duration (Months)")

fee = st.number_input(
    "Course Fee (₹)",
    min_value=0.0,
    max_value=100000.0,
    value=5000.0,
    step=500.0
)

capacity = st.number_input(
    "Course Capacity",
    min_value=1,
    max_value=500,
    value=30,
    step=1
)

if st.button("Add Course"):

    if not course_name.strip() or not instructor.strip() or not duration.strip():
        st.warning("Please fill in all required fields.")

    elif fee <= 0:
        st.warning("Course fee must be greater than zero.")

    else:
        conn = None
        cur = None

        try:
            conn = connect_db()
            cur = conn.cursor()

            query = """
                INSERT INTO courses
                (course_name, instructor, duration, fee, capacity)
                VALUES (%s, %s, %s, %s, %s)
            """

            cur.execute(
                query,
                (course_name.strip(), instructor.strip(),
                 duration.strip(), fee, capacity)
            )

            conn.commit()
            st.success("Course Added Successfully!")

        except Exception as e:
            if conn:
                conn.rollback()
            st.error("Unable to add course.")
            print("Database Error:", e)

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
