
import streamlit as st
from db import connect_db
from auth import require_login

require_login()
st.title("✏️ Update Course")

# Fetch course records
try:
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

except Exception as e:
    st.error("Unable to load course records.")
    print("Database Error:", e)
    st.stop()


if not courses:
    st.info("No courses available. Please add a course first.")
    st.stop()


# Select course
selected = st.selectbox(
    "Select Course",
    courses,
    format_func=lambda c: f"{c[1]} (ID: {c[0]})"
)

course_id = selected[0]

st.subheader("Edit Course Details")

with st.form(key=f"update_course_{course_id}"):

    course_name = st.text_input(
        "Course Name",
        value=selected[1] or ""
    )

    instructor = st.text_input(
        "Instructor",
        value=selected[2] or ""
    )

    duration = st.text_input(
        "Duration",
        value=selected[3] or ""
    )

    submit = st.form_submit_button("Update Course")

    if submit:

        if not course_name.strip() or not instructor.strip() or not duration.strip():
            st.warning("Please fill in all fields.")

        else:
            conn = None
            cur = None

            try:
                conn = connect_db()
                cur = conn.cursor()

                query = """
                    UPDATE courses
                    SET course_name = %s,
                        instructor = %s,
                        duration = %s
                    WHERE course_id = %s
                """

                cur.execute(
                    query,
                    (course_name.strip(), instructor.strip(),
                     duration.strip(), course_id)
                )

                conn.commit()

                if cur.rowcount > 0:
                    st.success("Course details updated successfully!")
                else:
                    st.info("No changes were made.")

            except Exception as e:
                if conn:
                    conn.rollback()

                st.error("Unable to update course details.")
                print("Update Error:", e)

            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
