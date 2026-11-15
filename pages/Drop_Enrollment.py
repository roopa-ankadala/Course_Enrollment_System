
import streamlit as st
from db import connect_db
from auth import require_login

require_login()
st.title("❌ Drop Enrollment")

st.warning(
    "This will remove only the selected enrollment. "
    "The student and course records will remain unchanged."
)

# Fetch enrollment details
try:
    conn = connect_db()
    cur = conn.cursor()

    query = """
        SELECT
            e.enrollment_id,
            e.student_id,
            s.student_name,
            e.course_id,
            c.course_name,
            e.enrollment_date
        FROM enrollments e
        INNER JOIN students s
            ON e.student_id = s.student_id
        INNER JOIN courses c
            ON e.course_id = c.course_id
        ORDER BY e.enrollment_id
    """

    cur.execute(query)
    enrollments = cur.fetchall()

    cur.close()
    conn.close()

except Exception as e:
    st.error("Unable to load enrollment records.")
    print("Database Error:", e)
    st.stop()


# Check enrollment availability
if not enrollments:
    st.info("No enrollment records available.")
    st.stop()


# Select enrollment
selected = st.selectbox(
    "Select Enrollment",
    enrollments,
    format_func=lambda e:
        f"Enrollment ID: {e[0]} | {e[2]} - {e[4]}"
)


# Display enrollment details
st.subheader("Enrollment Details")

st.write("Enrollment ID:", selected[0])
st.write("Student ID:", selected[1])
st.write("Student Name:", selected[2])
st.write("Course ID:", selected[3])
st.write("Course Name:", selected[4])
st.write("Enrollment Date:", selected[5])


# Confirmation
confirm = st.checkbox(
    "I confirm that I want to drop this enrollment."
)


if st.button("Drop Enrollment"):

    if not confirm:
        st.warning("Please confirm before dropping the enrollment.")

    else:
        conn = None
        cur = None

        try:
            conn = connect_db()
            cur = conn.cursor()

            query = """
                DELETE FROM enrollments
                WHERE enrollment_id = %s
            """

            cur.execute(query, (selected[0],))

            if cur.rowcount > 0:
                conn.commit()
                st.success("Enrollment dropped successfully!")
                st.rerun()

            else:
                conn.rollback()
                st.warning("Enrollment record was not found.")

        except Exception as e:
            if conn:
                conn.rollback()

            st.error("Unable to drop enrollment.")
            print("Delete Error:", e)

        finally:
            if cur:
                cur.close()

            if conn:
                conn.close()
