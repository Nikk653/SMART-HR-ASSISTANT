import streamlit as st
from dotenv import load_dotenv

from authentication.login import login_page
from modules.dashboard import dashboard_page
from modules.attendance import attendance_page
from modules.leave import leave_page
from modules.payroll import payroll_page
from modules.profile import profile_page
from modules.chatbot import chatbot_page


load_dotenv()

st.set_page_config(
    page_title="Smart HR Assistant",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# Minimal global styling.
# No custom HTML containers are used in the application UI.
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .stApp {
            background: #f4f7fb;
        }

        [data-testid="stSidebar"] {
            background: #0f172a;
            border-right: 1px solid #1e293b;
        }

        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {
            color: #dbe5f2 !important;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #f8fafc !important;
        }

        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e4eaf1;
            border-radius: 14px;
            padding: 14px 16px;
        }

        div.stButton > button {
            border-radius: 9px !important;
            border: 1px solid #d8e0ea !important;
            font-weight: 650 !important;
        }

        div.stButton > button:hover {
            border-color: #8fb1ea !important;
            color: #174ea6 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "employee" not in st.session_state:
    st.session_state.employee = None


# ---------------------------------------------------------
# Login
# ---------------------------------------------------------
if not st.session_state.logged_in:
    login_page()
    st.stop()


employee = st.session_state.get("employee") or {}

first_name = employee.get("first_name", "Employee")
last_name = employee.get("last_name", "")
full_name = f"{first_name} {last_name}".strip()
employee_id = employee.get("employee_id", "N/A")


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.title("🏢 Smart HR")
    st.caption("Employee Self-Service Portal")

    st.divider()

    st.write("**Signed in as**")
    st.write(full_name)
    st.caption(f"Employee ID: {employee_id}")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Attendance",
            "Leave",
            "Payroll",
            "Profile",
            "Chatbot",
        ],
    )

    st.divider()

    if st.button("Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.employee = None
        st.session_state.pop("chat_history", None)
        st.session_state.pop("last_hr_ticket", None)
        st.rerun()


# ---------------------------------------------------------
# Routing
# ---------------------------------------------------------
if page == "Dashboard":
    dashboard_page()

elif page == "Attendance":
    attendance_page()

elif page == "Leave":
    leave_page()

elif page == "Payroll":
    payroll_page()

elif page == "Profile":
    profile_page()

elif page == "Chatbot":
    chatbot_page()
