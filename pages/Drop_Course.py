
import streamlit as st
from db import connect_db
from auth import require_login

require_login()
st.title("Drop Course")
st.warning("Dropping a course will also delete all student enrollment records for that course.")

# Fetch courses
conn = connect_db()
cur = conn.cursor()

cur.execute("""
    SELECT course_id, course_name, instructor, duration
    FROM courses
    ORDER BY course_id
""")

courses = cur.fetchall()

cur.close()
conn.close()

if not courses:
    st.info("No courses available to drop.")

else:
    selected = st.selectbox(
        "Select Course",
        courses,
        format_func=lambda c: f"{c[0]} - {c[1]}"
    )

    course_id = selected[0]

    st.subheader("Course Details")
    st.write("Course ID:", selected[0])
    st.write("Course Name:", selected[1])
    st.write("Instructor:", selected[2])
    st.write("Duration:", selected[3])

    confirm = st.checkbox(
        "I understand that all enrollments for this course will also be deleted."
    )

    if st.button("Drop Course"):

        if not confirm:
            st.error("Please confirm before deleting.")

        else:
            conn = connect_db()
            cur = conn.cursor()

            try:
                # Delete related enrollments first
                cur.execute(
                    "DELETE FROM enrollments WHERE course_id = %s",
                    (course_id,)
                )

                # Delete course
                cur.execute(
                    "DELETE FROM courses WHERE course_id = %s",
                    (course_id,)
                )

                conn.commit()
                st.success("Course and related enrollments deleted successfully!")
                st.rerun()

            except Exception as e:
                conn.rollback()
                st.error(f"Error: {e}")

            finally:
                cur.close()
                conn.close()
