
import streamlit as st
from db import connect_db
from auth import require_login

require_login()
st.title("Drop Student")
st.warning("Dropping a student will also delete all their enrollment records.")

# Fetch students
conn = connect_db()
cur = conn.cursor()

cur.execute("""
    SELECT student_id, student_name, email, department
    FROM students
    ORDER BY student_id
""")

students = cur.fetchall()

cur.close()
conn.close()

if not students:
    st.info("No students available to drop.")

else:
    selected = st.selectbox(
        "Select Student",
        students,
        format_func=lambda s: f"{s[0]} - {s[1]}"
    )

    student_id = selected[0]

    st.subheader("Student Details")
    st.write("Student ID:", selected[0])
    st.write("Name:", selected[1])
    st.write("Email:", selected[2])
    st.write("Department:", selected[3])

    confirm = st.checkbox(
        "I understand that all enrollments of this student will also be deleted."
    )

    if st.button("Drop Student"):

        if not confirm:
            st.error("Please confirm before deleting.")

        else:
            conn = connect_db()
            cur = conn.cursor()

            try:
                # Delete related enrollments first
                cur.execute(
                    "DELETE FROM enrollments WHERE student_id = %s",
                    (student_id,)
                )

                # Delete student
                cur.execute(
                    "DELETE FROM students WHERE student_id = %s",
                    (student_id,)
                )

                conn.commit()
                st.success("Student and related enrollments deleted successfully!")
                st.rerun()

            except Exception as e:
                conn.rollback()
                st.error(f"Error: {e}")

            finally:
                cur.close()
                conn.close()
