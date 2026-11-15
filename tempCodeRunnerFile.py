
import streamlit as st

st.set_page_config(
    page_title="Course Enrollment System",
    page_icon="🎓",
    layout="wide"
)

st.sidebar.title("🎓 CES Menu")
st.sidebar.success("Select a Page")

st.title("🎓 Course Enrollment System")
st.write("Manage Students, Courses and Enrollments")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("