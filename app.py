
import streamlit as st
from auth import verify_user

st.set_page_config(
    page_title="Course Enrollment System",
    layout="wide"
)

# Initialize login session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Login Page
if not st.session_state.logged_in:

    st.title("🔐 Course Enrollment System")
    st.subheader("Login")

    with st.form("login_form"):

        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password"
        )

        login_button = st.form_submit_button("Login")

        if login_button:

            if verify_user(username.strip(), password):
                st.session_state.logged_in = True
                st.session_state.username = username.strip()

                st.success("Login successful!")
                st.rerun()

            else:
                st.error("Invalid username or password.")

    st.stop()


# Logged-in user information
st.sidebar.success(
    f"Welcome, {st.session_state.username}"
)

# Logout
if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

# KEEP YOUR EXISTING DASHBOARD AND NAVIGATION CODE BELOW

# Page Configuration
st.set_page_config(
    page_title="Course Enrollment System",
    page_icon="🎓",
    layout="wide"
)
# st.sidebar.page_link(
#     "pages/Basic_Queries.py",
#     label="Basic Queries",
#     icon="📋"
# )
# st.sidebar.page_link(
#     "pages/Joins.py",
#     label="SQL Joins",
#     icon="🔗"
# )
# ---------------- THEME SETTINGS ----------------

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ---------------- SIDEBAR ----------------

st.sidebar.title("🎓 CES Menu")

st.sidebar.toggle(
    "🌙 Dark Mode",
    key="dark_mode"
)

dark = st.session_state.dark_mode

# Theme Colors
if dark:
    bg = "#0F172A"
    sidebar = "#020617"
    text = "#F8FAFC"
    card = "#1E293B"
    button = "#3B82F6"
    quote_bg = "#1E293B"
    quote_text = "#BFDBFE"
    border = "#3B82F6"
    muted = "#CBD5E1"

else:
    bg = "#F1F5F9"
    sidebar = "#0F172A"
    text = "#0F172A"
    card = "#FFFFFF"
    button = "#2563EB"
    quote_bg = "#EAF2FF"
    quote_text = "#1E3A8A"
    border = "#2563EB"
    muted = "#475569"


# ---------------- CUSTOM CSS ----------------

st.markdown(f"""
<style>

/* Main Background */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.stApp {{
    background-color: {bg};
    color: {text};
}}

/* Main Content Text */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp p,
.stApp li {{
    color: {text};
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background-color: {sidebar};
}}

[data-testid="stSidebar"] * {{
    color: #FFFFFF;
}}

/* Dark Mode Toggle Label */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] label p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
    color: #FFFFFF !important;
}}

/* Toggle Widget */
[data-testid="stSidebar"] [data-testid="stToggle"] {{
    color: #FFFFFF !important;
}}

/* Hide Default Navigation */
[data-testid="stSidebarNav"] {{
    display: none;
}}

/* Buttons */
.stButton > button {{
    background-color: {button};
    color: #FFFFFF !important;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
}}

/* Button Hover */
.stButton > button:hover {{
    background-color: #1D4ED8;
    color: #FFFFFF !important;
    border: none;
}}

/* Input Fields */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {{
    background-color: {card};
    color: {text};
    border-radius: 8px;
}}

/* Select Box */
.stSelectbox div[data-baseweb="select"] {{
    background-color: {card};
    color: {text};
}}

/* Quote Box */
.quote-box {{
    background-color: {quote_bg};
    padding: 18px;
    border-left: 5px solid {border};
    border-radius: 10px;
    text-align: center;
    margin-bottom: 25px;
}}

.quote-box h3 {{
    color: {quote_text} !important;
    margin: 0;
}}

/* Divider */
hr {{
    border-color: #64748B;
}}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR NAVIGATION ----------------

if st.sidebar.button("👨‍🎓 Add Student", use_container_width=True):
    st.switch_page("pages/Add_Student.py")

if st.sidebar.button("📚 Add Course", use_container_width=True):
    st.switch_page("pages/Add_Course.py")

if st.sidebar.button("✅ Enroll Student", use_container_width=True):
    st.switch_page("pages/Enroll_Student.py")

if st.sidebar.button("📊 Reports", use_container_width=True):
    st.switch_page("pages/Reports.py")

if st.sidebar.button("🗑️ Drop Student", use_container_width=True):
    st.switch_page("pages/Drop_Student.py")

if st.sidebar.button("🗑️ Drop Course", use_container_width=True):
    st.switch_page("pages/Drop_Course.py")

if st.sidebar.button("👨‍🎓 View Students",use_container_width=True):
    st.switch_page("pages/View_Students.py")

if st.sidebar.button("📚 View Courses",use_container_width=True):
    st.switch_page("pages/View_Courses.py")

if st.sidebar.button("✏️ Update Student",use_container_width=True):
    st.switch_page("pages/Update_Student.py")

if st.sidebar.button("✏️ Update Course",use_container_width=True):
    st.switch_page("pages/Update_Course.py")

if st.sidebar.button("❌ Drop Enrollment",use_container_width=True):
    st.switch_page("pages/Drop_Enrollment.py")

if st.sidebar.button("📋 Basic Queries",use_container_width=True):
    st.switch_page("pages/Basic_Queries.py")

if st.sidebar.button("🔗 Joins",use_container_width=True):
    st.switch_page("pages/Joins.py")
# ---------------- MAIN PAGE ----------------

st.markdown("""
<div class="quote-box">
    <h3>"Learn. Grow. Achieve. Repeat."</h3>
</div>
""", unsafe_allow_html=True)

st.title("🎓 Course Enrollment System")

st.markdown("""
> "Plan Your Learning. Shape Your Future."
>
> — RoAkRo
""")

st.write(
    "A Smart and Simple Way to Manage Academic Enrollments."
)

st.markdown("""
Manage student information, organize courses, and streamline
the enrollment process through a centralized platform.
Maintain academic records efficiently and access information easily.
""")

st.markdown("---")


# ---------------- PAGE NAVIGATION ----------------

st.subheader("📌 Select a Page")

st.write("Choose an option below to get started.")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("👨‍🎓 Add Students", use_container_width=True):
        st.switch_page("pages/Add_Student.py")

with col2:
    if st.button("📚 Add Courses", use_container_width=True):
        st.switch_page("pages/Add_Course.py")

with col3:
    if st.button("✅ Enroll Students", use_container_width=True):
        st.switch_page("pages/Enroll_Student.py")


# ---------------- WELCOME SECTION ----------------

st.markdown("---")

st.subheader("👋 Welcome to CES!")

st.write("""
Our Course Enrollment System provides a simple and organized
platform for managing academic activities.
""")

st.markdown("""
- **Student Management:** Register and maintain student details.
- **Course Management:** Add and manage available courses.
- **Enrollment Management:** Enroll students in courses and maintain records.
- **Reports:** View and monitor enrollment information.
""")

st.info(
    "💡 Get started by selecting an option above or using "
    "the navigation menu on the left."
)
