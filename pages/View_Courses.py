
import streamlit as st
import pandas as pd
from db import connect_db
from auth import require_login

require_login()
st.title("📚 View Courses")

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

    if not courses:
        st.info("No courses found. Please add courses first.")

    else:
        df = pd.DataFrame(
            courses,
            columns=["Course ID", "Course Name", "Instructor", "Duration"]
        )

        # Total courses
        st.metric("Total Courses", len(df))

        # Search
        search = st.text_input("🔍 Search courses")

        if search:
            df = df[
                df.astype(str).apply(
                    lambda row: row.str.contains(
                        search, case=False, regex=False
                    ).any(),
                    axis=1
                )
            ]

        st.subheader("Course Details")

        if df.empty:
            st.warning("No matching courses found.")
        else:
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

except Exception as e:
    st.error("Unable to load course records.")
    print("Error:", e)
